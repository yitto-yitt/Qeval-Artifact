import argparse
import contextlib
import copy
import csv
import importlib.metadata
import inspect
import io
import json
import math
import multiprocessing as mp
import pickle
import platform
import re
import sys
import tempfile
import traceback
import types
import zipfile
from pathlib import Path
from typing import Any, Callable
from xml.sax.saxutils import escape
import numpy as np
from tasks import TASK_IDS, build_qiskit_cases, get_task_spec
ROOT = Path(__file__).resolve().parent
DEFAULT_REPORT_DIR = ROOT / 'reports'
RESTORED_QPANDA_QVMS: list[Any] = []
FRAMEWORKS = ('cirq', 'qpanda', 'qpanda2')
STATE_TASKS = {2, 11, 39, 139}
CIRCUIT_STATE_TASKS = {3, 5, 6, 62, 66}
MEASURED_CIRCUIT_TASKS = {3, 66}
STATE_FIDELITY_MIN = 0.95
TRACE_DISTANCE_MAX = 0.1
PURITY_DIFF_MAX = 0.05
EPSILON = 0.1
CASE_TIMEOUT_SECONDS = 60.0

def read_text_auto(path: Path) -> str:
    for encoding in ('utf-8-sig', 'utf-8', 'gb18030'):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding='utf-8', errors='replace')

def parse_task_ids(raw: str | None) -> list[int]:
    if raw is None or raw.strip().lower() == 'all':
        return TASK_IDS[:]
    task_ids = [int(part.strip()) for part in raw.split(',') if part.strip()]
    unsupported = sorted(set(task_ids).difference(TASK_IDS))
    if unsupported:
        raise ValueError(f'Unsupported task id(s): {unsupported}')
    return task_ids

def parse_frameworks(raw: str) -> list[str]:
    frameworks = [part.strip().lower() for part in raw.split(',') if part.strip()]
    if not frameworks:
        raise ValueError('At least one framework is required.')
    unsupported = sorted(set(frameworks).difference(FRAMEWORKS))
    if unsupported:
        raise ValueError(f'Unsupported framework(s): {unsupported}')
    return frameworks

def safe_dir_name(name: str) -> str:
    return re.sub('[^A-Za-z0-9._-]+', '_', name).strip('._') or 'model'

def sample_suffix(sample_index: int) -> str:
    if sample_index < 1:
        raise ValueError(f'Sample index must be positive, got {sample_index}')
    return f'_s{sample_index}'

def candidate_file_name(task_id: int, sample_index: int) -> str:
    return f'code{task_id}{sample_suffix(sample_index)}.py'

def candidate_path_for_sample(output_dir: Path, model: str, framework: str, task_id: int, sample_index: int) -> Path:
    return output_dir / model / framework / candidate_file_name(task_id, sample_index)

def discover_candidate_samples(output_dir: Path, model: str, framework: str, task_id: int) -> list[tuple[int, Path]]:
    framework_dir = output_dir / model / framework
    if not framework_dir.is_dir():
        return []
    candidates: list[tuple[int, Path]] = []
    base_path = framework_dir / candidate_file_name(task_id, 1)
    if base_path.is_file():
        candidates.append((1, base_path))
    suffix_pattern = re.compile(f'^code{task_id}_s(\\d+)\\.py$')
    for path in sorted(framework_dir.glob(f'code{task_id}_s*.py')):
        match = suffix_pattern.match(path.name)
        if match is None:
            continue
        sample_index = int(match.group(1))
        if sample_index > 1:
            candidates.append((sample_index, path))
    return sorted(candidates, key=lambda item: item[0])

def std_path(std_dir: Path, task_id: int) -> Path:
    return std_dir / f'code{task_id}.py'

def resolve_models(raw_models: str, output_dir: Path) -> list[str]:
    if raw_models.strip().lower() == 'all':
        if not output_dir.exists():
            return []
        return sorted((path.name for path in output_dir.iterdir() if path.is_dir()))
    return [safe_dir_name(part.strip()) for part in raw_models.split(',') if part.strip()]

def evaluate(args: argparse.Namespace) -> int:
    task_ids = parse_task_ids(args.tasks)
    if args.limit is not None:
        task_ids = task_ids[:args.limit]
    frameworks = parse_frameworks(args.frameworks)
    std_dir = Path(args.std_dir)
    output_dir = Path(args.output_dir)
    models = resolve_models(args.models, output_dir)
    report_root = Path(args.reports_dir) if args.reports_dir else DEFAULT_REPORT_DIR
    report_root.mkdir(parents=True, exist_ok=True)
    flat_rows: list[dict[str, Any]] = []
    print(f'Frameworks: {', '.join(frameworks)}')
    print(f'Models: {(', '.join(models) if models else '(none found)')}')
    print(f'Tasks: {', '.join((str(task_id) for task_id in task_ids))}')
    print(f'Reports dir: {report_root}')
    for model in models:
        for framework in frameworks:
            candidate_dir = output_dir / model / framework
            sample_results = []
            for task_id in task_ids:
                sample_paths = discover_candidate_samples(output_dir, model, framework, task_id)
                if not sample_paths:
                    sample_paths = [(1, candidate_path_for_sample(output_dir, model, framework, task_id, 1))]
                for sample_index, candidate_path in sample_paths:
                    sample_results.append(evaluate_task(task_id, std_dir, candidate_dir, framework, sample_index, candidate_path))
            details = build_raw_details(sample_results, std_dir, candidate_dir, model, framework)
            model_report_dir = report_root / model / framework
            write_report_bundle(model_report_dir, details, flatten_results(model, details))
            flat_rows.extend(flatten_results(model, details))
    if flat_rows:
        write_flat_results(report_root, flat_rows)
    return 0

def evaluate_task(task_id: int, std_dir: Path, candidate_dir: Path, framework: str, sample_index: int=1, candidate_path: Path | None=None) -> dict[str, Any]:
    spec = get_task_spec(task_id)
    candidate_path = candidate_path or candidate_dir / f'code{task_id}.py'
    result: dict[str, Any] = {'task_id': task_id, 'class_id': spec.class_id, 'path_a': str(std_path(std_dir, task_id)), 'path_b': str(candidate_path), 'candidate_path': str(candidate_path), 'sample_index': sample_index, 'framework': framework, 'function': spec.entrypoint, 'cases': [], 'sample_pass': False, 'sample_status': 'FAIL', 'sample_label': 'FAIL', 'raw_status': 'FAIL', 'raw_label': 'FAIL', 'setup_error': None}
    try:
        func_b = load_entry_function(candidate_path, f'{framework}_b_code{task_id}', spec.entrypoint)
        func_a = None
        if task_id in STATE_TASKS or task_id in CIRCUIT_STATE_TASKS:
            func_a = load_entry_function(std_path(std_dir, task_id), f'qiskit_a_code{task_id}', spec.entrypoint)
    except Exception:
        result['setup_error'] = traceback.format_exc().strip()
        return result
    qiskit_cases = build_qiskit_cases()
    framework_cases = build_framework_cases(framework)
    all_passed = True
    for index, qiskit_case in enumerate(qiskit_cases[task_id], start=1):
        framework_case = framework_cases[task_id][index - 1]
        row = evaluate_case(task_id, func_a, func_b, qiskit_case, framework_case, index, framework)
        result['cases'].append(row)
        all_passed = all_passed and row['status'] == 'PASS'
    if all_passed:
        result['sample_pass'] = True
        result['sample_status'] = 'PASS'
        result['sample_label'] = 'PASS'
        result['raw_status'] = 'PASS'
        result['raw_label'] = 'PASS'
    else:
        result['sample_status'] = infer_sample_status(result)
        result['raw_status'] = result['sample_status']
        result['sample_label'] = 'FAIL'
        result['raw_label'] = result['sample_label']
    return result

def build_framework_cases(framework: str) -> dict[int, list[dict[str, Any]]]:
    if framework == 'cirq':
        return build_cirq_cases()
    if framework in {'qpanda', 'qpanda2'}:
        return build_qpanda_cases(framework)
    raise ValueError(f'Unsupported framework: {framework}')

def build_cirq_cases() -> dict[int, list[dict[str, Any]]]:
    import cirq
    from qiskit.quantum_info import random_statevector
    q0, q1 = cirq.LineQubit.range(2)
    bell = cirq.Circuit(cirq.H(q0), cirq.CNOT(q0, q1))
    schmidt_data = np.asarray(random_statevector(4, seed=42).data, dtype=complex)
    return {2: [{'label': 'default', 'args': ()}], 3: [{'label': 'drawing_false', 'args': (False,)}], 5: [{'label': 'default', 'args': ()}], 6: [{'label': 'num_qubits_3', 'args': (3,)}], 11: [{'label': 'bell_state', 'args': (bell,)}], 39: [{'label': 'n3', 'args': (3,)}], 62: [{'label': 'z_one', 'args': ([1], [0])}, {'label': 'x_zero', 'args': ([0], [1])}, {'label': 'mixed_four_qubits', 'args': ([0, 1, 1, 0], [0, 0, 1, 1])}], 66: [{'label': 'default', 'args': ()}], 139: [{'label': 'random_state_seed_42_qargs_1', 'args': (schmidt_data, [1])}]}

def get_qpanda_module(framework: str) -> Any:
    if framework == 'qpanda2':
        import pyqpanda as pq
        return pq
    if framework == 'qpanda':
        import pyqpanda3.core as pq
        return pq
    raise ValueError(f'Unsupported framework: {framework}')

def build_qpanda_cases(framework: str) -> dict[int, list[dict[str, Any]]]:
    pq = get_qpanda_module(framework)
    from qiskit.quantum_info import random_statevector
    if framework == 'qpanda':
        from pyqpanda3.intermediate_compiler import convert_qprog_to_originir
        bell = pq.QProg(2)
        bell << pq.H(0) << pq.CNOT(0, 1)
        bell_originir = convert_qprog_to_originir(bell)
    else:
        bell_qvm = pq.CPUQVM()
        bell_qvm.init_qvm()
        bell_qubits = bell_qvm.qAlloc_many(2)
        bell = pq.QProg()
        bell << pq.H(bell_qubits[0]) << pq.CNOT(bell_qubits[0], bell_qubits[1])
        bell_originir = pq.convert_qprog_to_originir(bell, bell_qvm)
        bell_qvm.finalize()
    schmidt_data = np.asarray(random_statevector(4, seed=42).data, dtype=complex)
    return {2: [{'label': 'default', 'args': ()}], 3: [{'label': 'drawing_false', 'args': (False,)}], 5: [{'label': 'default', 'args': ()}], 6: [{'label': 'num_qubits_3', 'args': (3,)}], 11: [{'label': 'bell_state', 'args': ({'__kind__': 'qpanda_originir', 'framework': framework, 'originir': bell_originir},)}], 39: [{'label': 'n3', 'args': (3,)}], 62: [{'label': 'z_one', 'args': ([1], [0])}, {'label': 'x_zero', 'args': ([0], [1])}, {'label': 'mixed_four_qubits', 'args': ([0, 1, 1, 0], [0, 0, 1, 1])}], 66: [{'label': 'default', 'args': ()}], 139: [{'label': 'random_state_seed_42_qargs_1', 'args': (schmidt_data, [1])}]}

def evaluate_case(task_id: int, func_a: Callable[..., Any] | None, func_b: Callable[..., Any], qiskit_case: dict[str, Any], framework_case: dict[str, Any], index: int, framework: str) -> dict[str, Any]:
    if task_id in STATE_TASKS:
        if func_a is None:
            raise ValueError(f'task {task_id} requires a reference function')
        return evaluate_state_case(task_id, func_a, func_b, qiskit_case, framework_case, index, framework)
    if task_id in CIRCUIT_STATE_TASKS:
        if func_a is None:
            raise ValueError(f'task {task_id} requires a reference function')
        return evaluate_circuit_state_case(task_id, func_a, func_b, qiskit_case, framework_case, index, framework)
    raise ValueError(f'Unsupported evaluation task: {task_id}')

def evaluate_state_case(task_id: int, func_a: Callable[..., Any], func_b: Callable[..., Any], qiskit_case: dict[str, Any], framework_case: dict[str, Any], index: int, framework: str) -> dict[str, Any]:
    label = qiskit_case.get('label', f'case_{index}')
    row = base_case_row(label)
    outcome_a = call_and_capture(func_a, clone_value(tuple(qiskit_case.get('args', ()))), clone_value(dict(qiskit_case.get('kwargs', {}))))
    outcome_b = call_framework_candidate(func_b, framework, clone_value(tuple(framework_case.get('args', ()))), clone_value(dict(framework_case.get('kwargs', {}))))
    if outcome_a['error'] or outcome_b['error']:
        row['error'] = combine_errors(outcome_a, outcome_b)
        return row
    try:
        value_a = outcome_a['value']
        value_b = outcome_b['value']
        if task_id == 139:
            value_a = reconstruct_schmidt_state(value_a)
            value_b = reconstruct_schmidt_state(value_b)
        metrics = compare_quantum_states(value_a, value_b)
    except Exception:
        row['error'] = f'METRIC ERROR:\n{traceback.format_exc().strip()}'
        return row
    row.update(metrics)
    row['status'] = 'PASS' if state_metrics_pass(metrics) else 'FAIL'
    return row

def evaluate_circuit_state_case(task_id: int, func_a: Callable[..., Any], func_b: Callable[..., Any], qiskit_case: dict[str, Any], framework_case: dict[str, Any], index: int, framework: str) -> dict[str, Any]:
    from qiskit.quantum_info import Statevector
    label = qiskit_case.get('label', f'case_{index}')
    row = base_case_row(label)
    outcome_a = call_and_capture(func_a, clone_value(tuple(qiskit_case.get('args', ()))), clone_value(dict(qiskit_case.get('kwargs', {}))))
    outcome_b = call_framework_candidate(func_b, framework, clone_value(tuple(framework_case.get('args', ()))), clone_value(dict(framework_case.get('kwargs', {}))))
    if outcome_a['error'] or outcome_b['error']:
        row['error'] = combine_errors(outcome_a, outcome_b)
        return row
    try:
        qiskit_circuit = coerce_qiskit_circuit(outcome_a['value'])
        candidate_circuit = coerce_framework_circuit(outcome_b['value'], framework)
        strip_terminal_measurements = task_id in MEASURED_CIRCUIT_TASKS
        if task_id in MEASURED_CIRCUIT_TASKS:
            require_framework_measurements(candidate_circuit, framework)
            qiskit_circuit = qiskit_circuit.copy()
            qiskit_circuit.remove_final_measurements()
            if framework == 'cirq':
                candidate_circuit = drop_terminal_framework_measurements(candidate_circuit, framework)
        value_a = Statevector.from_instruction(qiskit_circuit)
        candidate_states = framework_circuit_to_statevector_variants(candidate_circuit, framework, expected_num_qubits=qiskit_circuit.num_qubits, strip_terminal_measurements=strip_terminal_measurements)
        metrics = best_quantum_state_comparison(value_a, candidate_states)
    except Exception:
        row['error'] = f'METRIC ERROR:\n{traceback.format_exc().strip()}'
        return row
    row.update(metrics)
    row['status'] = 'PASS' if state_metrics_pass(metrics) else 'FAIL'
    return row

def base_case_row(label: Any) -> dict[str, Any]:
    return {'label': label, 'status': 'FAIL', 'error': None, 'fidelity': None, 'trace_distance': None, 'purity_diff': None, 'dataset_length': None, 'metric_name': None, 'min_metric': None, 'max_metric': None, 'failed_items': []}

def coerce_pair(value: Any) -> tuple[Any, Any]:
    if not isinstance(value, (tuple, list)) or len(value) != 2:
        raise TypeError(f'Expected a pair, got {value!r}')
    return (value[0], value[1])

def coerce_qiskit_circuit(value: Any) -> Any:
    from qiskit import QuantumCircuit
    if isinstance(value, QuantumCircuit):
        return value
    if isinstance(value, (tuple, list)) and value and isinstance(value[0], QuantumCircuit):
        return value[0]
    raise TypeError(f'Expected QuantumCircuit output, got {type(value).__name__}')

def coerce_cirq_circuit(value: Any) -> Any:
    import cirq
    if isinstance(value, cirq.Circuit):
        return value
    if isinstance(value, (tuple, list)) and value and isinstance(value[0], cirq.Circuit):
        return value[0]
    raise TypeError(f'Expected cirq.Circuit output, got {type(value).__name__}')

def coerce_qpanda_circuit(value: Any) -> Any:
    try:
        pq = get_qpanda_module('qpanda2')
        q2_circuit_types = (pq.QCircuit, pq.QProg)
    except Exception:
        q2_circuit_types = ()
    try:
        pq = get_qpanda_module('qpanda')
        q3_circuit_types = (pq.QCircuit, pq.QProg)
    except Exception:
        q3_circuit_types = ()
    circuit_types = q2_circuit_types + q3_circuit_types
    if circuit_types and isinstance(value, circuit_types):
        return value
    if circuit_types and isinstance(value, (tuple, list)) and value and isinstance(value[0], circuit_types):
        return value[0]
    raise TypeError(f'Expected pyQPanda QCircuit or QProg output, got {type(value).__name__}')

def coerce_framework_circuit(value: Any, framework: str) -> Any:
    if framework == 'cirq':
        return coerce_cirq_circuit(value)
    if framework in {'qpanda', 'qpanda2'}:
        return coerce_qpanda_circuit(value)
    raise ValueError(f'Unsupported framework: {framework}')

def require_cirq_measurements(circuit: Any) -> None:
    import cirq
    if not any((cirq.is_measurement(operation) for operation in circuit.all_operations())):
        raise ValueError('Expected returned circuit to contain measurement operations')

def require_qpanda_measurements(circuit: Any) -> None:
    for framework in ('qpanda2', 'qpanda'):
        try:
            text = qpanda_originir_text(circuit, framework)
        except Exception:
            continue
        if 'MEASURE' in text.upper():
            return
    raise ValueError('Expected returned circuit to contain measurement operations')

def require_framework_measurements(circuit: Any, framework: str) -> None:
    if framework == 'cirq':
        require_cirq_measurements(circuit)
        return
    if framework in {'qpanda', 'qpanda2'}:
        require_qpanda_measurements(circuit)
        return
    raise ValueError(f'Unsupported framework: {framework}')

def drop_terminal_cirq_measurements(circuit: Any) -> Any:
    import cirq
    return cirq.drop_terminal_measurements(circuit)

def drop_terminal_qpanda_measurements_for_framework(circuit: Any, framework: str) -> Any:
    return circuit

def qpanda_originir_text(circuit: Any, framework: str) -> str:
    pq = get_qpanda_module(framework)
    if framework == 'qpanda':
        from pyqpanda3.intermediate_compiler import convert_qprog_to_originir
        qprog = circuit if isinstance(circuit, pq.QProg) else pq.QProg() << circuit
        return convert_qprog_to_originir(qprog)
    qvm = prepare_qpanda_machine_for_program(circuit, pq)
    try:
        qprog = circuit if isinstance(circuit, pq.QProg) else pq.QProg() << circuit
        return pq.convert_qprog_to_originir(qprog, qvm)
    finally:
        qvm.finalize()

def prepare_qpanda_machine_for_program(circuit: Any, pq: Any) -> Any:
    qprog = circuit if isinstance(circuit, pq.QProg) else pq.QProg() << circuit
    qvm = pq.CPUQVM()
    try:
        max_qubit = int(qprog.get_max_qubit_addr())
    except Exception:
        max_qubit = -1
    if max_qubit >= 0:
        qvm.init_qvm(max_qubit + 1)
        qvm.qAlloc_many(max_qubit + 1)
    else:
        qvm.init_qvm()
    try:
        used_cbits = qprog.get_used_cbits([])
        cbit_count = len(used_cbits)
    except Exception:
        cbit_count = 0
    if cbit_count > 0:
        qvm.cAlloc_many(cbit_count)
    return qvm

def strip_terminal_measure_lines(originir: str) -> str:
    lines = originir.splitlines()
    while lines and lines[-1].strip().upper().startswith('MEASURE'):
        lines.pop()
    return '\n'.join(lines)

def drop_terminal_framework_measurements(circuit: Any, framework: str) -> Any:
    if framework == 'cirq':
        return drop_terminal_cirq_measurements(circuit)
    if framework in {'qpanda', 'qpanda2'}:
        return drop_terminal_qpanda_measurements_for_framework(circuit, framework)
    raise ValueError(f'Unsupported framework: {framework}')

def cirq_circuit_to_statevector(circuit: Any, expected_num_qubits: int | None=None) -> Any:
    import cirq
    qubits = sorted(circuit.all_qubits())
    if expected_num_qubits is not None and len(qubits) < expected_num_qubits:
        qubits = list(cirq.LineQubit.range(expected_num_qubits))
    qubit_order = list(reversed(qubits))
    return cirq.Simulator().simulate(circuit, qubit_order=qubit_order).final_state_vector

def framework_circuit_to_statevector_variants(circuit: Any, framework: str, expected_num_qubits: int | None=None, strip_terminal_measurements: bool=False) -> list[Any]:
    if framework == 'cirq':
        vector = cirq_circuit_to_statevector(circuit, expected_num_qubits=expected_num_qubits)
        return statevector_order_variants(vector)
    if framework in {'qpanda', 'qpanda2'}:
        vector = qpanda_circuit_to_statevector(circuit, framework, expected_num_qubits=expected_num_qubits, strip_terminal_measurements=strip_terminal_measurements)
        return statevector_order_variants(vector)
    raise ValueError(f'Unsupported framework: {framework}')

def qpanda_circuit_to_statevector(circuit: Any, framework: str, expected_num_qubits: int | None=None, strip_terminal_measurements: bool=False) -> Any:
    pq = get_qpanda_module(framework)
    if framework == 'qpanda':
        from pyqpanda3.intermediate_compiler import convert_originir_string_to_qprog, convert_qprog_to_originir
        qprog = circuit if isinstance(circuit, pq.QProg) else pq.QProg() << circuit
        if strip_terminal_measurements:
            originir = convert_qprog_to_originir(qprog)
            cleaned_originir = strip_terminal_measure_lines(originir)
            if cleaned_originir != originir:
                qprog = convert_originir_string_to_qprog(cleaned_originir)
        qvm = pq.CPUQVM()
        qvm.run(qprog, 1)
        vector = np.asarray(qvm.result().get_state_vector(), dtype=complex).reshape(-1)
    else:
        qvm = prepare_qpanda_machine_for_program(circuit, pq)
        try:
            qprog = circuit if isinstance(circuit, pq.QProg) else pq.QProg() << circuit
            if strip_terminal_measurements:
                originir = pq.convert_qprog_to_originir(qprog, qvm)
                cleaned_originir = strip_terminal_measure_lines(originir)
                if cleaned_originir != originir:
                    qprog, *_ = pq.convert_originir_str_to_qprog(cleaned_originir, qvm)
            qvm.directly_run(qprog)
            vector = np.asarray(qvm.get_qstate(), dtype=complex).reshape(-1)
        finally:
            qvm.finalize()
    dim = vector.shape[0]
    num_qubits = int(math.log2(dim)) if dim else 0
    if 2 ** num_qubits != dim:
        raise ValueError(f'pyQPanda circuit state dimension is not a power of two: {dim}')
    if expected_num_qubits is not None and num_qubits != expected_num_qubits:
        raise ValueError(f'Expected {expected_num_qubits} qubits, got {num_qubits}')
    return vector

def statevector_order_variants(value: Any) -> list[Any]:
    vector = np.asarray(value, dtype=complex).reshape(-1)
    variants = [vector]
    reversed_vector = reverse_qubit_order_statevector(vector)
    if reversed_vector is not None and reversed_vector.tobytes() != vector.tobytes():
        variants.append(reversed_vector)
    return variants

def reverse_qubit_order_statevector(vector: Any) -> Any | None:
    vector = np.asarray(vector, dtype=complex).reshape(-1)
    dim = vector.shape[0]
    if dim == 0 or dim & dim - 1:
        return None
    num_qubits = int(math.log2(dim))
    if 2 ** num_qubits != dim or num_qubits <= 1:
        return None
    permutation = [reverse_bits(index, num_qubits) for index in range(dim)]
    return vector[permutation]

def reverse_bits(value: int, width: int) -> int:
    result = 0
    for _ in range(width):
        result = result << 1 | value & 1
        value >>= 1
    return result

def best_quantum_state_comparison(left: Any, candidates: list[Any]) -> dict[str, float]:
    if not candidates:
        raise ValueError('No candidate states to compare')
    metrics = [compare_quantum_states(left, candidate) for candidate in candidates]
    metrics.sort(key=lambda item: (item['fidelity'], -item['trace_distance'], -item['purity_diff']), reverse=True)
    return metrics[0]

def compare_quantum_states(left: Any, right: Any) -> dict[str, float]:
    from qiskit.quantum_info import state_fidelity
    rho = as_density_matrix(left)
    sigma = as_density_matrix(right)
    return {'fidelity': float(state_fidelity(rho, sigma)), 'trace_distance': trace_distance(rho, sigma), 'purity_diff': abs(purity_value(rho) - purity_value(sigma))}

def state_metrics_pass(metrics: dict[str, float]) -> bool:
    return metrics['fidelity'] >= STATE_FIDELITY_MIN and metrics['trace_distance'] <= TRACE_DISTANCE_MAX and (metrics['purity_diff'] <= PURITY_DIFF_MAX)

def as_statevector(value: Any) -> Any:
    from qiskit.quantum_info import Statevector
    extracted = extract_statevector_like(value)
    if isinstance(extracted, Statevector):
        return extracted
    return Statevector(np.asarray(extracted, dtype=complex))

def as_density_matrix(value: Any) -> Any:
    from qiskit.quantum_info import DensityMatrix, Statevector
    extracted = extract_density_like(value)
    if isinstance(extracted, DensityMatrix):
        return extracted
    if isinstance(extracted, Statevector):
        return DensityMatrix(extracted)
    array = np.asarray(extracted, dtype=complex)
    if array.ndim == 1:
        return DensityMatrix(Statevector(array))
    return DensityMatrix(array)

def extract_statevector_like(value: Any) -> Any:
    if hasattr(value, 'final_state_vector'):
        return value.final_state_vector
    if hasattr(value, 'state_vector') and (not callable(value.state_vector)):
        return value.state_vector
    if hasattr(value, 'state_vector') and callable(value.state_vector):
        return value.state_vector()
    if hasattr(value, 'data') and value.__class__.__module__.startswith('qiskit'):
        return value
    return value

def extract_density_like(value: Any) -> Any:
    if hasattr(value, 'final_density_matrix'):
        return value.final_density_matrix
    if hasattr(value, 'density_matrix') and (not callable(value.density_matrix)):
        return value.density_matrix
    if hasattr(value, 'density_matrix') and callable(value.density_matrix):
        return value.density_matrix()
    return extract_statevector_like(value)

def trace_distance(left: Any, right: Any) -> float:
    rho = as_density_matrix(left).data
    sigma = as_density_matrix(right).data
    delta = rho - sigma
    eigenvalues = np.linalg.eigvalsh(delta)
    return float(0.5 * np.sum(np.abs(eigenvalues)).real)

def purity_value(value: Any) -> float:
    density = as_density_matrix(value).data
    return float(np.trace(density @ density).real)

def reconstruct_schmidt_state(value: Any) -> Any:
    from qiskit.quantum_info import Statevector
    terms = normalize_schmidt_terms(value)
    vector = None
    for coeff, left, right in terms:
        left_vector = as_statevector(left)
        right_vector = as_statevector(right)
        term = complex(coeff) * left_vector.tensor(right_vector).data
        vector = term if vector is None else vector + term
    if vector is None:
        raise ValueError('Schmidt decomposition is empty')
    return Statevector(vector)

def normalize_schmidt_terms(value: Any) -> list[tuple[Any, Any, Any]]:
    if isinstance(value, tuple) and len(value) == 2:
        coeffs, subsystems = value
        if isinstance(coeffs, (list, tuple, np.ndarray)) and isinstance(subsystems, (list, tuple)):
            terms = []
            for coeff, pair in zip(coeffs, subsystems):
                left, right = coerce_pair(pair)
                terms.append((coeff, left, right))
            if terms:
                return terms
    if not isinstance(value, (list, tuple)):
        raise TypeError(f'Schmidt decomposition output is not sequence-like: {type(value).__name__}')
    terms = []
    for item in value:
        if not isinstance(item, (list, tuple)) or len(item) != 3:
            raise TypeError(f'Schmidt item must be (coeff, vecA, vecB), got {item!r}')
        terms.append((item[0], item[1], item[2]))
    return terms

def load_entry_function(path: Path, module_name: str, entrypoint: str) -> Callable[..., Any]:
    if not path.is_file():
        raise FileNotFoundError(path)
    module = types.ModuleType(module_name)
    module.__file__ = str(path)
    module.__package__ = ''
    sys.modules[module_name] = module
    source = read_text_auto(path)
    code = compile(source, str(path), 'exec')
    with prepend_sys_path(path.parent):
        exec(code, module.__dict__)
    value = vars(module).get(entrypoint)
    if value is None:
        public_functions = [name for name, candidate in vars(module).items() if inspect.isfunction(candidate) and candidate.__module__ == module.__name__ and (not name.startswith('_'))]
        raise ValueError(f'Missing required function {entrypoint!r} in {path}. Public functions found: {public_functions}')
    if not inspect.isfunction(value):
        raise TypeError(f'{entrypoint!r} in {path} is not a function')
    value.__eval_source_path__ = str(path)
    value.__eval_module_name__ = module_name
    value.__eval_entrypoint__ = entrypoint
    return value

@contextlib.contextmanager
def prepend_sys_path(path: Path):
    text = str(path)
    sys.path.insert(0, text)
    try:
        yield
    finally:
        try:
            sys.path.remove(text)
        except ValueError:
            pass

def call_worker(result_path: str, source_path: str, module_name: str, entrypoint: str, args: tuple[Any, ...], kwargs: dict[str, Any]) -> None:
    try:
        args = tuple((restore_worker_value(arg) for arg in args))
        kwargs = {key: restore_worker_value(value) for key, value in kwargs.items()}
        func = load_entry_function(Path(source_path), module_name, entrypoint)
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            value = func(*args, **kwargs)
        result = {'value': serialize_worker_value(value), 'error': None, 'captured_stdout': stdout.getvalue()[-4000:]}
    except Exception:
        result = {'value': None, 'error': traceback.format_exc().strip(), 'captured_stdout': ''}
    with open(result_path, 'wb') as handle:
        pickle.dump(result, handle)

def serialize_worker_value(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: serialize_worker_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [serialize_worker_value(item) for item in value]
    if isinstance(value, tuple):
        return tuple((serialize_worker_value(item) for item in value))
    if is_qpanda_circuit_like(value):
        return serialize_qpanda_value(value)
    if is_unpicklable_object(value):
        return serialize_generic_object(value)
    return value

def is_qpanda_circuit_like(value: Any) -> bool:
    type_name = type(value).__name__
    module_name = type(value).__module__
    return type_name in {'QProg', 'QCircuit'} and module_name.startswith('pyqpanda')

def is_unpicklable_object(value: Any) -> bool:
    if isinstance(value, (str, bytes, bytearray, int, float, complex, bool, type(None))):
        return False
    if isinstance(value, (dict, list, tuple, set, frozenset, np.ndarray)):
        return False
    if is_qpanda_circuit_like(value):
        return False
    try:
        pickle.dumps(value)
    except Exception:
        return hasattr(value, '__dict__')
    return False

def serialize_generic_object(value: Any) -> dict[str, Any]:
    return {'__kind__': 'python_object', '__class__': type(value).__name__, '__module__': type(value).__module__, '__attrs__': {key: serialize_worker_value(item) for key, item in vars(value).items()}}

def serialize_qpanda_value(value: Any) -> dict[str, Any]:
    framework = 'qpanda2' if 'pyqpanda.pyQPanda' in type(value).__module__ else 'qpanda'
    pq = get_qpanda_module(framework)
    qprog = value if isinstance(value, pq.QProg) else pq.QProg() << value
    if framework == 'qpanda':
        from pyqpanda3.intermediate_compiler import convert_qprog_to_originir
        originir = convert_qprog_to_originir(qprog)
        return {'__kind__': 'qpanda_originir', 'framework': framework, 'originir': originir}
    qvm = prepare_qpanda_machine_for_program(value, pq)
    try:
        originir = pq.convert_qprog_to_originir(qprog, qvm)
        return {'__kind__': 'qpanda_originir', 'framework': framework, 'originir': originir}
    finally:
        qvm.finalize()

def call_and_capture(func: Callable[..., Any], args: tuple[Any, ...], kwargs: dict[str, Any], timeout_seconds: float=CASE_TIMEOUT_SECONDS) -> dict[str, Any]:
    source_path = getattr(func, '__eval_source_path__', None)
    module_name = getattr(func, '__eval_module_name__', None)
    entrypoint = getattr(func, '__eval_entrypoint__', None)
    if not source_path or not module_name or (not entrypoint):
        return {'value': None, 'error': 'INTERNAL ERROR: function lacks eval metadata', 'captured_stdout': ''}
    result_file = tempfile.NamedTemporaryFile(prefix='cross_eval_', suffix='.pkl', delete=False)
    result_path = result_file.name
    result_file.close()
    spawn_args = serialize_worker_value(args)
    spawn_kwargs = serialize_worker_value(kwargs)
    process = mp.Process(target=call_worker, args=(result_path, source_path, module_name, entrypoint, spawn_args, spawn_kwargs))
    process.start()
    process.join(timeout_seconds)
    try:
        if process.is_alive():
            process.terminate()
            process.join(5)
            if process.is_alive():
                process.kill()
                process.join()
            return {'value': None, 'error': f'TIMEOUT after {timeout_seconds:g}s', 'error_type': 'timeout', 'captured_stdout': ''}
        if Path(result_path).stat().st_size > 0:
            with open(result_path, 'rb') as handle:
                result = pickle.load(handle)
            result['value'] = restore_worker_value(result.get('value'))
            return result
        if process.exitcode not in (0, None):
            return {'value': None, 'error': f'PROCESS EXITED with code {process.exitcode}', 'captured_stdout': ''}
        return {'value': None, 'error': 'PROCESS EXITED without result', 'captured_stdout': ''}
    finally:
        try:
            Path(result_path).unlink()
        except FileNotFoundError:
            pass

def restore_worker_value(value: Any) -> Any:
    if isinstance(value, dict):
        if value.get('__kind__') == 'qpanda_originir':
            return restore_qpanda_value(value)
        if value.get('__kind__') == 'python_object':
            return {key: restore_worker_value(item) for key, item in value.get('__attrs__', {}).items()}
        return {key: restore_worker_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [restore_worker_value(item) for item in value]
    if isinstance(value, tuple):
        return tuple((restore_worker_value(item) for item in value))
    return value

def restore_qpanda_value(value: dict[str, Any]) -> Any:
    framework = value.get('framework', 'qpanda2')
    pq = get_qpanda_module(framework)
    if framework == 'qpanda':
        from pyqpanda3.intermediate_compiler import convert_originir_string_to_qprog
        return convert_originir_string_to_qprog(value['originir'])
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qprog, *_ = pq.convert_originir_str_to_qprog(value['originir'], qvm)
    RESTORED_QPANDA_QVMS.append(qvm)
    return qprog

def call_framework_candidate(func: Callable[..., Any], framework: str, args: tuple[Any, ...], kwargs: dict[str, Any]) -> dict[str, Any]:
    if framework == 'qpanda':
        return call_and_capture_direct(func, args, kwargs)
    return call_and_capture(func, args, kwargs)

def call_and_capture_direct(func: Callable[..., Any], args: tuple[Any, ...], kwargs: dict[str, Any]) -> dict[str, Any]:
    try:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            value = func(*args, **kwargs)
        return {'value': value, 'error': None, 'captured_stdout': stdout.getvalue()[-4000:]}
    except Exception:
        return {'value': None, 'error': traceback.format_exc().strip(), 'captured_stdout': ''}

def clone_value(value: Any) -> Any:
    try:
        return copy.deepcopy(value)
    except Exception:
        return value

def format_outcome_error(label: str, outcome: dict[str, Any]) -> str:
    if outcome.get('error_type') == 'timeout':
        return f'{label} TIMEOUT: {outcome['error']}'
    if outcome.get('error_type'):
        return f'{label} {outcome['error_type']}:\n{outcome['error']}'
    return f'{label} ERROR:\n{outcome['error']}'

def combine_errors(outcome_a: dict[str, Any], outcome_b: dict[str, Any]) -> str:
    errors = []
    if outcome_a.get('error'):
        errors.append(format_outcome_error('A', outcome_a))
    if outcome_b.get('error'):
        errors.append(format_outcome_error('B', outcome_b))
    return '\n'.join(errors)

def thresholds() -> dict[str, float]:
    return {'state_fidelity_min': STATE_FIDELITY_MIN, 'trace_distance_max': TRACE_DISTANCE_MAX, 'purity_diff_max': PURITY_DIFF_MAX, 'epsilon': EPSILON, 'case_timeout_seconds': CASE_TIMEOUT_SECONDS}

def build_raw_details(sample_results: list[dict[str, Any]], std_dir: Path, candidate_dir: Path, model: str, framework: str) -> dict[str, Any]:
    grouped: dict[int, list[dict[str, Any]]] = {}
    for sample in sample_results:
        grouped.setdefault(int(sample['task_id']), []).append(sample)
    results = []
    for task_id in sorted(grouped):
        samples = sorted(grouped[task_id], key=lambda sample: int(sample.get('sample_index') or 0))
        first = samples[0]
        pass_count, pass_at_1, pass_at_3, pass_at_5 = task_pass_metrics(samples)
        best_sample = next((sample for sample in samples if sample.get('sample_pass')), None)
        results.append({'task_id': task_id, 'class_id': first.get('class_id'), 'path_a': first.get('path_a'), 'path_b': first.get('path_b'), 'framework': framework, 'function': first.get('function'), 'samples': samples, 'sample_count': len(samples), 'pass_count': pass_count, 'pass_at_1': pass_at_1, 'pass_at_3': pass_at_3, 'pass_at_5': pass_at_5, 'best_sample_index': None if best_sample is None else best_sample.get('sample_index'), 'best_sample_path': None if best_sample is None else best_sample.get('candidate_path'), 'raw_status': aggregate_task_status(samples), 'raw_label': 'PASS' if pass_count > 0 else 'FAIL', 'setup_error': None if samples else 'No samples'})
    return {'mode': 'cross_language', 'class_id': 2, 'model': model, 'framework': framework, 'dir_a': str(std_dir), 'dir_b': str(candidate_dir), 'thresholds': thresholds(), 'environment': build_environment_info(), 'summary': {}, 'results': results}

def task_pass_metrics(samples: list[dict[str, Any]]) -> tuple[int, float | None, float | None, float | None]:
    sample_passes = [bool(sample.get('sample_pass')) for sample in samples]
    pass_count = sum((1 for passed in sample_passes if passed))
    if any((sample.get('raw_status', infer_sample_status(sample)) == 'ERROR' for sample in samples)):
        return (pass_count, None, None, None)
    return (pass_count, estimate_pass_at_k(len(sample_passes), pass_count, 1), estimate_pass_at_k(len(sample_passes), pass_count, 3), estimate_pass_at_k(len(sample_passes), pass_count, 5))

def infer_sample_status(sample: dict[str, Any]) -> str:
    if sample.get('setup_error'):
        return 'FAIL'
    cases = sample.get('cases', []) or []
    statuses = [str(case.get('status', 'FAIL')) for case in cases]
    return 'PASS' if statuses and all((status == 'PASS' for status in statuses)) else 'FAIL'

def aggregate_task_status(samples: list[dict[str, Any]]) -> str:
    statuses = [sample.get('raw_status', infer_sample_status(sample)) for sample in samples]
    return 'PASS' if 'PASS' in statuses else 'FAIL'

def estimate_pass_at_k(sample_count: int, pass_count: int, k: int) -> float | None:
    if sample_count <= 0 or k <= 0 or sample_count < k:
        return None
    if pass_count <= 0:
        return 0.0
    if sample_count - pass_count < k:
        return 1.0
    return 1.0 - math.comb(sample_count - pass_count, k) / math.comb(sample_count, k)

def write_report_bundle(report_dir: Path, details: dict[str, Any], flat_rows: list[dict[str, Any]] | None=None) -> None:
    classification = build_classification_rows(details)
    summary = build_summary(classification)
    fail_samples = build_fail_samples(classification, details)
    error_samples = build_error_samples(classification, details)
    details['summary'] = summary
    write_json(report_dir / 'raw_details.json', details)
    write_text(report_dir / 'raw_report.txt', build_text_report(details))
    write_text(report_dir / 'environment.txt', build_environment_report(details['environment']))
    write_jsonl(report_dir / 'classification.jsonl', classification)
    write_summary_csv(report_dir / 'summary.csv', summary)
    write_json(report_dir / 'fail_samples.json', fail_samples)
    write_json(report_dir / 'error_samples.json', error_samples)
    write_flat_results(report_dir, flat_rows if flat_rows is not None else flatten_results(str(details.get('model')), details))
    write_metrics_xlsx(report_dir / 'metrics.xlsx', details)
    print(f'Wrote report: {report_dir}')

def build_classification_rows(details: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for result in details['results']:
        final_label = 'PASS' if int(result.get('pass_count') or 0) > 0 else 'FAIL'
        rows.append({'task_id': result.get('task_id'), 'class_id': result.get('class_id'), 'framework': result.get('framework'), 'function': result.get('function'), 'path_b': result.get('best_sample_path') or result.get('path_b'), 'raw_label': result.get('raw_label'), 'raw_status': result.get('raw_status'), 'final_label': final_label, 'decision_stage': 'pass@5', 'passed': final_label == 'PASS', 'sample_count': result.get('sample_count'), 'pass_count': result.get('pass_count'), 'pass_at_1': result.get('pass_at_1'), 'pass_at_3': result.get('pass_at_3'), 'pass_at_5': result.get('pass_at_5'), 'best_sample_index': result.get('best_sample_index'), 'best_sample_path': result.get('best_sample_path'), 'sample_statuses': sample_statuses(result), 'failure_note': None if final_label == 'PASS' else 'evaluation incomplete; result is undetermined' if final_label == 'ERROR' else 'all samples failed', 'error_summary': build_error_summary(result)})
    return rows

def sample_statuses(result: dict[str, Any]) -> list[dict[str, Any]]:
    statuses = []
    for sample in result.get('samples', []) or []:
        statuses.append({'sample_index': sample.get('sample_index'), 'candidate_path': sample.get('candidate_path'), 'status': sample.get('sample_status', sample.get('raw_status', infer_sample_status(sample))), 'label': sample.get('sample_label'), 'cases': case_statuses(sample)})
    return statuses

def case_statuses(sample: dict[str, Any]) -> list[dict[str, Any]]:
    return [{'label': case.get('label'), 'status': case.get('status'), 'fidelity': case.get('fidelity'), 'trace_distance': case.get('trace_distance'), 'purity_diff': case.get('purity_diff'), 'metric_name': case.get('metric_name'), 'dataset_length': case.get('dataset_length'), 'min_metric': case.get('min_metric'), 'max_metric': case.get('max_metric'), 'failed_items': case.get('failed_items')} for case in sample.get('cases', []) or []]

def build_error_summary(result: dict[str, Any]) -> dict[str, Any]:
    errors: list[dict[str, str]] = []
    for sample in result.get('samples', []) or []:
        setup_error = sample.get('setup_error')
        if setup_error:
            errors.append({'sample_index': sample.get('sample_index'), 'case': 'SETUP', 'error': setup_error})
        for case in sample.get('cases', []) or []:
            error = case.get('error')
            failed_items = case.get('failed_items') or []
            if error:
                errors.append({'sample_index': sample.get('sample_index'), 'case': str(case.get('label')), 'error': str(error)})
            elif failed_items:
                errors.append({'sample_index': sample.get('sample_index'), 'case': str(case.get('label')), 'error': f'failed_items={len(failed_items)}'})
    return {'raw': errors} if errors else {}

def build_fail_samples(rows: list[dict[str, Any]], details: dict[str, Any]) -> list[dict[str, Any]]:
    by_task = {int(result['task_id']): result for result in details['results']}
    return [{'task_id': row['task_id'], 'class_id': row.get('class_id'), 'framework': row.get('framework'), 'function': row.get('function'), 'path_b': row.get('path_b'), 'failure_note': row.get('failure_note'), 'raw': by_task.get(int(row['task_id']))} for row in rows if row['final_label'] == 'FAIL']

def build_error_samples(rows: list[dict[str, Any]], details: dict[str, Any]) -> list[dict[str, Any]]:
    by_task = {int(result['task_id']): result for result in details['results']}
    return [{'task_id': row['task_id'], 'class_id': row.get('class_id'), 'framework': row.get('framework'), 'function': row.get('function'), 'path_b': row.get('path_b'), 'failure_note': row.get('failure_note'), 'raw': by_task.get(int(row['task_id']))} for row in rows if row.get('final_label') == 'ERROR']

def build_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    task_total = len(rows)
    task_raw_pass = sum((1 for row in rows if int(row.get('pass_count') or 0) > 0))
    task_error = sum((1 for row in rows if row.get('raw_status') == 'ERROR'))
    sample_total = sum((int(row.get('sample_count') or 0) for row in rows))
    sample_pass = sum((int(row.get('pass_count') or 0) for row in rows))
    sample_status_list = [status for row in rows for status in row.get('sample_statuses') or []]
    sample_error = sum((1 for item in sample_status_list if item.get('status') == 'ERROR'))
    sample_fail = sum((1 for item in sample_status_list if item.get('status') == 'FAIL'))
    pass_at_1_values = [float(row['pass_at_1']) for row in rows if row.get('pass_at_1') is not None]
    pass_at_3_values = [float(row['pass_at_3']) for row in rows if row.get('pass_at_3') is not None]
    pass_at_5_values = [float(row['pass_at_5']) for row in rows if row.get('pass_at_5') is not None]
    pass_at_1_sum = sum(pass_at_1_values)
    pass_at_3_sum = sum(pass_at_3_values)
    pass_at_5_sum = sum(pass_at_5_values)
    return {'task_total': task_total, 'task_RAW_PASS': task_raw_pass, 'task_FAIL': sum((1 for row in rows if row.get('raw_status') == 'FAIL')), 'task_ERROR': task_error, 'sample_total': sample_total, 'sample_PASS': sample_pass, 'sample_FAIL': sample_fail, 'sample_ERROR': sample_error, 'pass_at_1_sum': pass_at_1_sum, 'pass_at_3_sum': pass_at_3_sum, 'pass_at_5_sum': pass_at_5_sum, 'pass_at_1': None if not pass_at_1_values else pass_at_1_sum / len(pass_at_1_values), 'pass_at_3': None if not pass_at_3_values else pass_at_3_sum / len(pass_at_3_values), 'pass_at_5': None if not pass_at_5_values else pass_at_5_sum / len(pass_at_5_values), 'pass_at_1_defined_task_count': len(pass_at_1_values), 'pass_at_3_defined_task_count': len(pass_at_3_values), 'pass_at_k_defined_task_count': len(pass_at_5_values)}

def build_text_report(details: dict[str, Any]) -> str:
    rows = []
    for result in details.get('results', []) or []:
        code = f'code{result['task_id']}'
        rows.append([code, str(result.get('sample_count') or 0), str(result.get('pass_count') or 0), format_metric(result.get('pass_at_1')), format_metric(result.get('pass_at_3')), format_metric(result.get('pass_at_5')), build_task_note(result)])
    headers = ['code', 'samples', 'c', 'pass@1', 'pass@3', 'pass@5', 'note']
    table = format_table(headers, rows)
    summary = details.get('summary', {})
    t = details.get('thresholds', {})
    return '\n'.join(['Class 2 cross-language evaluation report', f'model: {details.get('model')}', f'framework: {details.get('framework')}', f'dir_a: {details.get('dir_a')}', f'dir_b: {details.get('dir_b')}', f'thresholds: state_fidelity >= {t.get('state_fidelity_min')}, trace_distance <= {t.get('trace_distance_max')}, purity_diff <= {t.get('purity_diff_max')}, epsilon <= {t.get('epsilon')}', '', table, '', 'overall summary:', f'task_RAW_PASS: {summary.get('task_RAW_PASS', 0)} / {summary.get('task_total', 0)}', f'task_FAIL: {summary.get('task_FAIL', 0)} / {summary.get('task_total', 0)}', f'task_ERROR: {summary.get('task_ERROR', 0)} / {summary.get('task_total', 0)}', f'sample_PASS: {summary.get('sample_PASS', 0)} / {summary.get('sample_total', 0)}', f'sample_FAIL: {summary.get('sample_FAIL', 0)} / {summary.get('sample_total', 0)}', f'sample_ERROR: {summary.get('sample_ERROR', 0)} / {summary.get('sample_total', 0)}', f'pass@1: {format_rate(summary.get('pass_at_1'))}', f'pass@3: {format_rate(summary.get('pass_at_3'))}', f'pass@5: {format_rate(summary.get('pass_at_5'))}', f'pass@k defined tasks: @1={summary.get('pass_at_1_defined_task_count', 0)}, @3={summary.get('pass_at_3_defined_task_count', 0)}, @5={summary.get('pass_at_k_defined_task_count', 0)}', ''])

def build_task_note(result: dict[str, Any]) -> str:
    if result.get('setup_error'):
        return first_line(result.get('setup_error'))
    if int(result.get('pass_count') or 0) > 0:
        return ''
    for sample in result.get('samples', []) or []:
        if sample.get('setup_error'):
            return first_line(sample.get('setup_error'))
        for case in sample.get('cases', []) or []:
            if case.get('error'):
                return first_line(case.get('error'))
            failed_items = case.get('failed_items') or []
            if failed_items:
                return f'failed_items={len(failed_items)}'
    if not result.get('samples'):
        return 'No samples'
    return 'All samples failed'

def format_table(headers: list[str], rows: list[list[str]]) -> str:
    widths = [len(header) for header in headers]
    for row in rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(value))
    lines = [' | '.join((header.ljust(widths[index]) for index, header in enumerate(headers))), '-+-'.join(('-' * width for width in widths))]
    for row in rows:
        lines.append(' | '.join((value.ljust(widths[index]) for index, value in enumerate(row))))
    return '\n'.join(lines)

def flatten_results(model: str, details: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    framework = details.get('framework')
    for result in details['results']:
        for sample in result.get('samples', []) or []:
            if sample.get('setup_error'):
                rows.append({'model': model, 'framework': framework, 'task_id': result['task_id'], 'function': result['function'], 'sample_index': sample.get('sample_index'), 'candidate_path': sample.get('candidate_path'), 'case': 'SETUP', 'status': 'FAIL', 'raw_label': sample.get('sample_label'), 'error': sample.get('setup_error')})
                continue
            for case in sample.get('cases', []) or []:
                rows.append({'model': model, 'framework': framework, 'task_id': result['task_id'], 'function': result['function'], 'sample_index': sample.get('sample_index'), 'candidate_path': sample.get('candidate_path'), 'case': case.get('label'), 'status': case.get('status'), 'raw_label': sample.get('sample_label'), 'metric_name': case.get('metric_name') or ('state' if case.get('fidelity') is not None else ''), 'fidelity': case.get('fidelity'), 'trace_distance': case.get('trace_distance'), 'purity_diff': case.get('purity_diff'), 'dataset_length': case.get('dataset_length'), 'min_metric': case.get('min_metric'), 'max_metric': case.get('max_metric'), 'failed_items': len(case.get('failed_items') or []), 'error': case.get('error')})
    return rows

def write_flat_results(report_root: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames = ['model', 'framework', 'task_id', 'function', 'sample_index', 'candidate_path', 'case', 'status', 'raw_label', 'metric_name', 'fidelity', 'trace_distance', 'purity_diff', 'dataset_length', 'min_metric', 'max_metric', 'failed_items', 'error']
    report_root.mkdir(parents=True, exist_ok=True)
    with (report_root / 'results.csv').open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, '') for key in fieldnames})
    write_jsonl(report_root / 'results.jsonl', rows)

def build_environment_info() -> dict[str, Any]:
    packages = {}
    for package in ('cirq', 'pyqpanda', 'pyqpanda3', 'numpy', 'qiskit', 'qiskit-aer', 'qiskit-ibm-runtime'):
        try:
            packages[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            packages[package] = None
    return {'python': platform.python_version(), 'platform': platform.platform(), 'packages': packages}

def build_environment_report(info: dict[str, Any]) -> str:
    lines = ['Class 2 cross-language evaluation environment', f'python: {info.get('python')}', f'platform: {info.get('platform')}']
    for package, version in info.get('packages', {}).items():
        lines.append(f'{package}: {version or 'not installed'}')
    return '\n'.join(lines) + '\n'

def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8', newline='\n')

def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8', newline='\n')

def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='\n') as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + '\n')

def write_summary_csv(path: Path, summary: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='\n') as handle:
        writer = csv.writer(handle)
        writer.writerow(['metric', 'value'])
        for metric, value in build_summary_csv_rows(summary):
            writer.writerow([metric, value])

def build_summary_csv_rows(summary: dict[str, Any]) -> list[tuple[str, str]]:
    task_total = int(summary.get('task_total') or summary.get('total') or 0)
    task_raw_pass = int(summary.get('task_RAW_PASS') or summary.get('RAW_PASS') or 0)
    task_fail = int(summary.get('task_FAIL') or summary.get('raw_fail') or 0)
    task_error = int(summary.get('task_ERROR') or 0)
    sample_total = int(summary.get('sample_total') or 0)
    sample_pass = int(summary.get('sample_PASS') or 0)
    sample_fail = int(summary.get('sample_FAIL') or 0)
    sample_error = int(summary.get('sample_ERROR') or 0)
    return [('task_RAW_PASS', format_count(task_raw_pass, task_total)), ('task_FAIL', format_count(task_fail, task_total)), ('task_ERROR', format_count(task_error, task_total)), ('sample_PASS', format_count(sample_pass, sample_total)), ('sample_FAIL', format_count(sample_fail, sample_total)), ('sample_ERROR', format_count(sample_error, sample_total)), ('pass@1_defined_task_count', str(summary.get('pass_at_1_defined_task_count', 0))), ('pass@3_defined_task_count', str(summary.get('pass_at_3_defined_task_count', 0))), ('pass@5_defined_task_count', str(summary.get('pass_at_k_defined_task_count', 0))), ('pass@1', format_rate(summary.get('pass_at_1'))), ('pass@3', format_rate(summary.get('pass_at_3'))), ('pass@5', format_rate(summary.get('pass_at_5')))]

def format_count(value: int, total: int) -> str:
    return f'{value} / {total}'

def format_rate(value: Any) -> str:
    if value in ('', None):
        return ''
    return f'{float(value):.4f}'

def write_metrics_xlsx(path: Path, details: dict[str, Any]) -> None:
    summary_headers, summary_rows = build_metrics_summary_rows(details)
    sample_headers, sample_rows = build_metrics_sample_rows(details)
    case_headers, case_rows = build_metrics_case_rows(details)
    write_xlsx(path, [('Summary', summary_headers, summary_rows), ('Samples', sample_headers, sample_rows), ('Cases', case_headers, case_rows)])

def build_metrics_summary_rows(details: dict[str, Any]) -> tuple[list[str], list[list[Any]]]:
    headers = ['model', 'framework', 'code', 'task_id', 'function', 'samples', 'c', 'pass@1', 'pass@3', 'pass@5', 'note']
    rows = []
    for result in details.get('results', []) or []:
        rows.append([details.get('model'), details.get('framework'), f'code{result.get('task_id')}', result.get('task_id'), result.get('function'), result.get('sample_count'), result.get('pass_count'), result.get('pass_at_1'), result.get('pass_at_3'), result.get('pass_at_5'), build_task_note(result)])
    return (headers, rows)

def build_metrics_sample_rows(details: dict[str, Any]) -> tuple[list[str], list[list[Any]]]:
    headers = ['model', 'framework', 'code', 'task_id', 'function', 'sample_index', 'candidate_file', 'sample_pass', 'sample_status', 'case_count', 'pass_case_count', 'fail_case_count', 'error_case_count', 'min_fidelity', 'max_trace_distance', 'max_purity_diff', 'min_metric', 'max_metric', 'fidelity_threshold', 'trace_distance_threshold', 'purity_diff_threshold', 'epsilon', 'note']
    thresholds = details.get('thresholds') or {}
    rows = []
    for result in details.get('results', []) or []:
        for sample in result.get('samples', []) or []:
            cases = sample.get('cases', []) or []
            pass_case_count = sum((1 for case in cases if case.get('status') == 'PASS'))
            fail_case_count = sum((1 for case in cases if case.get('status') == 'FAIL'))
            error_case_count = sum((1 for case in cases if case.get('status') == 'ERROR'))
            fidelities = [case.get('fidelity') for case in cases if case.get('fidelity') is not None]
            trace_distances = [case.get('trace_distance') for case in cases if case.get('trace_distance') is not None]
            purity_diffs = [case.get('purity_diff') for case in cases if case.get('purity_diff') is not None]
            min_metrics = [case.get('min_metric') for case in cases if case.get('min_metric') is not None]
            max_metrics = [case.get('max_metric') for case in cases if case.get('max_metric') is not None]
            notes = [first_line(sample.get('setup_error'))] if sample.get('setup_error') else []
            notes.extend((first_line(case.get('error')) for case in cases if case.get('error')))
            note = '; '.join(notes)
            rows.append([details.get('model'), details.get('framework'), f'code{result.get('task_id')}', result.get('task_id'), result.get('function'), sample.get('sample_index'), Path(str(sample.get('candidate_path') or '')).name, bool(sample.get('sample_pass')), sample.get('sample_status', sample.get('raw_status', infer_sample_status(sample))), len(cases), pass_case_count, fail_case_count, error_case_count, min(fidelities) if fidelities else None, max(trace_distances) if trace_distances else None, max(purity_diffs) if purity_diffs else None, min(min_metrics) if min_metrics else None, max(max_metrics) if max_metrics else None, thresholds.get('state_fidelity_min'), thresholds.get('trace_distance_max'), thresholds.get('purity_diff_max'), thresholds.get('epsilon'), first_line(note)])
    return (headers, rows)

def build_metrics_case_rows(details: dict[str, Any]) -> tuple[list[str], list[list[Any]]]:
    headers = ['model', 'framework', 'code', 'task_id', 'function', 'sample_index', 'case', 'status', 'metric_name', 'fidelity', 'fidelity_threshold', 'fidelity_pass', 'trace_distance', 'trace_distance_threshold', 'trace_distance_pass', 'purity_diff', 'purity_diff_threshold', 'purity_diff_pass', 'dataset_length', 'min_metric', 'max_metric', 'epsilon', 'failed_items', 'error', 'candidate_path']
    thresholds = details.get('thresholds') or {}
    fidelity_threshold = thresholds.get('state_fidelity_min')
    trace_distance_threshold = thresholds.get('trace_distance_max')
    purity_diff_threshold = thresholds.get('purity_diff_max')
    epsilon = thresholds.get('epsilon')
    rows = []
    for result in details.get('results', []) or []:
        for sample in result.get('samples', []) or []:
            for case in sample.get('cases', []) or []:
                fidelity = case.get('fidelity')
                trace_distance = case.get('trace_distance')
                purity_diff = case.get('purity_diff')
                rows.append([details.get('model'), details.get('framework'), f'code{result.get('task_id')}', result.get('task_id'), result.get('function'), sample.get('sample_index'), case.get('label'), case.get('status'), case.get('metric_name') or ('state' if fidelity is not None else 'property'), fidelity, fidelity_threshold, None if fidelity is None else fidelity >= fidelity_threshold, trace_distance, trace_distance_threshold, None if trace_distance is None else trace_distance <= trace_distance_threshold, purity_diff, purity_diff_threshold, None if purity_diff is None else purity_diff <= purity_diff_threshold, case.get('dataset_length'), case.get('min_metric'), case.get('max_metric'), epsilon, len(case.get('failed_items') or []), case.get('error'), sample.get('candidate_path')])
    return (headers, rows)

def write_xlsx(path: Path, sheets: list[tuple[str, list[str], list[list[Any]]]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr('[Content_Types].xml', xlsx_content_types(len(sheets)))
        archive.writestr('_rels/.rels', xlsx_root_rels())
        archive.writestr('xl/workbook.xml', xlsx_workbook([sheet[0] for sheet in sheets]))
        archive.writestr('xl/_rels/workbook.xml.rels', xlsx_workbook_rels(len(sheets)))
        archive.writestr('xl/styles.xml', xlsx_styles())
        for index, (_, headers, rows) in enumerate(sheets, start=1):
            archive.writestr(f'xl/worksheets/sheet{index}.xml', xlsx_sheet(headers, rows))

def xlsx_content_types(sheet_count: int) -> str:
    overrides = '\n'.join((f'<Override PartName="/xl/worksheets/sheet{index}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' for index in range(1, sheet_count + 1)))
    return f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">\n<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>\n<Default Extension="xml" ContentType="application/xml"/>\n<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>\n<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>\n{overrides}\n</Types>'

def xlsx_root_rels() -> str:
    return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>\n</Relationships>'

def xlsx_workbook(sheet_names: list[str]) -> str:
    sheets_xml = '\n'.join((f'<sheet name="{escape(sheet_name)}" sheetId="{index}" r:id="rId{index}"/>' for index, sheet_name in enumerate(sheet_names, start=1)))
    return f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">\n<sheets>\n{sheets_xml}\n</sheets>\n</workbook>'

def xlsx_workbook_rels(sheet_count: int) -> str:
    rels = '\n'.join((f'<Relationship Id="rId{index}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{index}.xml"/>' for index in range(1, sheet_count + 1)))
    rels += f'\n<Relationship Id="rId{sheet_count + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
    return f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n{rels}\n</Relationships>'

def xlsx_styles() -> str:
    return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">\n<fonts count="1"><font><sz val="11"/><name val="Calibri"/></font></fonts>\n<fills count="1"><fill><patternFill patternType="none"/></fill></fills>\n<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>\n<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>\n<cellXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/></cellXfs>\n</styleSheet>'

def xlsx_sheet(headers: list[str], rows: list[list[Any]]) -> str:
    all_rows = [headers, *rows]
    row_xml = '\n'.join((f'<row r="{row_index}">' + ''.join((xlsx_cell(row_index, column_index, value) for column_index, value in enumerate(row, start=1))) + '</row>' for row_index, row in enumerate(all_rows, start=1)))
    return f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">\n<sheetData>\n{row_xml}\n</sheetData>\n</worksheet>'

def xlsx_cell(row_index: int, column_index: int, value: Any) -> str:
    cell_ref = f'{xlsx_column_name(column_index)}{row_index}'
    if value in ('', None):
        return f'<c r="{cell_ref}"/>'
    if isinstance(value, bool):
        return f'<c r="{cell_ref}" t="b"><v>{(1 if value else 0)}</v></c>'
    if isinstance(value, (int, float)) and (not isinstance(value, bool)) and math.isfinite(float(value)):
        return f'<c r="{cell_ref}"><v>{format_metric(value)}</v></c>'
    text = escape(str(value), {'"': '&quot;'})
    return f'<c r="{cell_ref}" t="inlineStr"><is><t>{text}</t></is></c>'

def xlsx_column_name(index: int) -> str:
    name = ''
    while index:
        index, remainder = divmod(index - 1, 26)
        name = chr(ord('A') + remainder) + name
    return name

def format_metric(value: Any) -> str:
    if value in ('', None):
        return ''
    number = float(value)
    return f'{number:.12g}'

def first_line(value: str | None) -> str:
    if not value:
        return ''
    return value.strip().splitlines()[0]
