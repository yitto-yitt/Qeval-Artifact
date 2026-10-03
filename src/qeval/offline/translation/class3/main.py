import argparse
import copy
import csv
import importlib.metadata
import inspect
import json
import math
import multiprocessing as mp
import pickle
import platform
import re
import sys
import tempfile
import types
import zipfile
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable
from xml.sax.saxutils import escape
from tasks import TASK_IDS, build_cases, get_task_spec
ROOT = Path(__file__).resolve().parent
DEFAULT_REPORTS_DIR = ROOT / 'reports'
FRAMEWORKS = ('cirq', 'qpanda', 'qpanda2')
QPANDA2_CALL_TIMEOUT_SECONDS = 60.0
PROCESS_FIDELITY_MIN = 0.95
AVERAGE_GATE_FIDELITY_MIN = 0.95
PARAMETER_VALUES = [0.37, 0.73, 1.11, 1.57, 2.03, 2.41, 2.89, 3.17]

def thresholds() -> dict[str, float]:
    return {'process_fidelity_min': PROCESS_FIDELITY_MIN, 'average_gate_fidelity_min': AVERAGE_GATE_FIDELITY_MIN}

def parse_task_ids(raw: str | None) -> list[int]:
    if raw is None or raw.strip().lower() == 'all':
        return TASK_IDS[:]
    selected: list[int] = []
    for part in raw.split(','):
        item = part.strip()
        if item:
            selected.append(int(item))
    unsupported = sorted(set(selected).difference(TASK_IDS))
    if unsupported:
        raise ValueError(f'Unsupported task id(s): {unsupported}')
    return selected

def parse_frameworks(raw: str) -> list[str]:
    frameworks = [item.strip().lower() for item in raw.split(',') if item.strip()]
    if not frameworks:
        raise ValueError('At least one framework is required.')
    unknown = sorted(set(frameworks).difference(FRAMEWORKS))
    if unknown:
        raise ValueError(f'Unsupported framework(s): {unknown}')
    return frameworks

def std_path(std_dir: Path, task_id: int) -> Path:
    return std_dir / f'code{task_id}.py'

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

def candidate_path(output_dir: Path, model: str, framework: str, task_id: int) -> Path:
    return candidate_path_for_sample(output_dir, model, framework, task_id, 1)

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

def evaluate(args: argparse.Namespace) -> int:
    task_ids = parse_task_ids(args.tasks)
    if args.limit is not None:
        task_ids = task_ids[:args.limit]
    frameworks = parse_frameworks(args.frameworks)
    output_dir = Path(args.output_dir)
    std_dir = Path(args.std_dir)
    if args.models.strip().lower() == 'all':
        models = sorted((path.name for path in output_dir.iterdir() if path.is_dir())) if output_dir.is_dir() else []
    else:
        models = [safe_dir_name(item.strip()) for item in args.models.split(',') if item.strip()]
    if not models:
        raise ValueError(f'No models found under {output_dir}')
    report_root = Path(args.reports_dir) if args.reports_dir else DEFAULT_REPORTS_DIR
    report_root.mkdir(parents=True, exist_ok=True)
    flat_rows: list[dict[str, Any]] = []
    for model in models:
        for framework in frameworks:
            candidate_dir = output_dir / model / framework
            sample_results = []
            for task_id in task_ids:
                sample_paths = discover_candidate_samples(output_dir, model, framework, task_id)
                if not sample_paths:
                    sample_paths = [(1, candidate_path_for_sample(output_dir, model, framework, task_id, 1))]
                for sample_index, sample_path in sample_paths:
                    sample_results.append(evaluate_task(task_id, framework, std_dir, candidate_dir, sample_index, sample_path, args.case_timeout))
            details = build_raw_details(sample_results, std_dir, candidate_dir, model, framework)
            report_dir = report_root / model / framework
            write_report_bundle(report_dir, details)
            flat_rows.extend(flatten_results(model, details))
            print(f'{model}/{framework}: {details['summary']['task_RAW_PASS']} task_RAW_PASS, {details['summary']['task_FAIL']} task_FAIL, {details['summary']['task_ERROR']} task_ERROR', flush=True)
    if flat_rows:
        write_flat_results(report_root, flat_rows)
    return 0

def evaluate_task(task_id: int, framework: str, std_dir: Path, candidate_dir: Path, sample_index: int=1, candidate_path: Path | None=None, case_timeout: float=QPANDA2_CALL_TIMEOUT_SECONDS) -> dict[str, Any]:
    spec = get_task_spec(task_id)
    result: dict[str, Any] = {'task_id': task_id, 'class_id': spec.class_id, 'framework': framework, 'path_a': None, 'path_b': None, 'candidate_path': None, 'sample_index': sample_index, 'function': spec.entrypoint, 'cases': [], 'sample_pass': False, 'sample_status': 'FAIL', 'sample_label': 'FAIL', 'raw_status': 'FAIL', 'raw_label': 'FAIL', 'setup_error': None}
    try:
        path_a = std_path(std_dir, task_id)
        path_b = candidate_path or resolve_code_path(candidate_dir, task_id)
        result['path_a'] = str(path_a)
        result['path_b'] = str(path_b)
        result['candidate_path'] = str(path_b)
        func_a = load_entry_function(path_a, f'class3_qiskit_code{task_id}', spec.entrypoint)
        if framework == 'qpanda2':
            func_b = DeferredEntryFunction(path_b, f'class3_{framework}_code{task_id}_s{sample_index}', spec.entrypoint)
        else:
            func_b = load_entry_function(path_b, f'class3_{framework}_code{task_id}_s{sample_index}', spec.entrypoint)
    except Exception as exc:
        result['setup_error'] = short_error(exc)
        return result
    all_cases = build_cases()
    all_passed = True
    for index, qiskit_case in enumerate(all_cases[task_id], start=1):
        row = evaluate_case(task_id, framework, func_a, func_b, qiskit_case, index, case_timeout)
        result['cases'].append(row)
        all_passed = all_passed and row['status'] == 'PASS'
    if all_passed:
        result['sample_pass'] = True
        result['sample_status'] = 'PASS'
        result['sample_label'] = 'PASS'
        result['raw_status'] = 'PASS'
        result['raw_label'] = 'PASS'
    else:
        result['sample_status'] = aggregate_case_status(result['cases'])
        result['raw_status'] = result['sample_status']
        result['sample_label'] = 'FAIL'
        result['raw_label'] = result['sample_label']
    return result

def evaluate_case(task_id: int, framework: str, func_a: Callable[..., Any], func_b: Callable[..., Any], qiskit_case: dict[str, Any], index: int, case_timeout: float=QPANDA2_CALL_TIMEOUT_SECONDS) -> dict[str, Any]:
    label = qiskit_case.get('label', f'case_{index}')
    row = base_case_row(label)
    qiskit_args = tuple(qiskit_case.get('args', ()))
    qiskit_kwargs = dict(qiskit_case.get('kwargs', {}))
    outcome_a = call_and_capture(func_a, clone_value(qiskit_args), clone_value(qiskit_kwargs))
    if outcome_a['error']:
        row['error'] = 'reference: ' + outcome_a['error']
        return row
    try:
        candidate_args = convert_args_for_framework(qiskit_args, framework, task_id)
        candidate_kwargs = convert_kwargs_for_framework(qiskit_kwargs, framework, task_id)
    except Exception as exc:
        row['error'] = 'case conversion: ' + short_error(exc)
        return row
    outcome_b = call_framework_candidate(func_b, framework, clone_value(candidate_args), clone_value(candidate_kwargs), case_timeout)
    if outcome_b['error']:
        error_type = outcome_b.get('error_type') or 'unclassified_worker_error'
        row['error'] = f'{error_type}: {outcome_b['error']}'
        return row
    try:
        if 'compare_modified_input' in qiskit_case:
            input_index = int(qiskit_case['compare_modified_input'])
            reference = outcome_a['args'][input_index]
            candidate = outcome_b['args'][input_index]
            metrics = compare_outputs(reference, candidate)
        elif 'compare_to_input' in qiskit_case:
            input_index = int(qiskit_case['compare_to_input'])
            reference = clone_value(qiskit_args[input_index])
            metrics = compare_candidate_sequence_to_reference(outcome_b['value'], reference)
        else:
            metrics = compare_outputs(outcome_a['value'], outcome_b['value'])
    except Exception as exc:
        row['error'] = short_error(exc)
        return row
    row.update(metrics)
    row['status'] = 'PASS' if process_metrics_pass(metrics) else 'FAIL'
    return row

def base_case_row(label: Any) -> dict[str, Any]:
    return {'label': label, 'status': 'FAIL', 'error': None, 'process_fidelity': None, 'average_gate_fidelity': None, 'sequence_length': None, 'item_metrics': []}

def aggregate_case_status(cases: list[dict[str, Any]]) -> str:
    statuses = [str(case.get('status', 'FAIL')) for case in cases]
    return 'PASS' if statuses and all((status == 'PASS' for status in statuses)) else 'FAIL'

def infer_sample_status(sample: dict[str, Any]) -> str:
    if sample.get('setup_error'):
        return 'FAIL'
    return aggregate_case_status(sample.get('cases', []) or [])

def aggregate_task_status(samples: list[dict[str, Any]]) -> str:
    statuses = [sample.get('sample_status', infer_sample_status(sample)) for sample in samples]
    return 'PASS' if 'PASS' in statuses else 'FAIL'

def convert_kwargs_for_framework(kwargs: dict[str, Any], framework: str, task_id: int) -> dict[str, Any]:
    return {key: convert_value_for_framework(value, framework, task_id) for key, value in kwargs.items()}

def convert_args_for_framework(args: tuple[Any, ...], framework: str, task_id: int) -> tuple[Any, ...]:
    if framework == 'qiskit':
        return clone_value(args)
    return tuple((convert_value_for_framework(value, framework, task_id) for value in args))

def convert_value_for_framework(value: Any, framework: str, task_id: int) -> Any:
    if framework == 'cirq':
        return convert_value_to_cirq(value, task_id)
    if framework == 'qpanda':
        return convert_value_to_qpanda(value, task_id)
    if framework == 'qpanda2':
        return convert_value_to_qpanda2(value, task_id)
    return clone_value(value)

def convert_value_to_cirq(value: Any, task_id: int) -> Any:
    if is_qiskit_quantum_circuit(value):
        return qiskit_circuit_to_cirq(value, task_id)
    if is_qiskit_operator_like(value):
        return qiskit_operator_matrix(value)
    if isinstance(value, list):
        return [convert_value_to_cirq(item, task_id) for item in value]
    if isinstance(value, tuple):
        return tuple((convert_value_to_cirq(item, task_id) for item in value))
    return clone_value(value)

def convert_value_to_qpanda(value: Any, task_id: int) -> Any:
    if is_qiskit_quantum_circuit(value):
        return qiskit_circuit_to_qpanda(value, task_id)
    if is_qiskit_operator_like(value):
        return qiskit_operator_matrix(value)
    if isinstance(value, list):
        return [convert_value_to_qpanda(item, task_id) for item in value]
    if isinstance(value, tuple):
        return tuple((convert_value_to_qpanda(item, task_id) for item in value))
    return clone_value(value)

def convert_value_to_qpanda2(value: Any, task_id: int) -> Any:
    if is_qiskit_quantum_circuit(value) or is_qiskit_operator_like(value):
        return qiskit_operator_matrix(value)
    if isinstance(value, list):
        return [convert_value_to_qpanda2(item, task_id) for item in value]
    if isinstance(value, tuple):
        return tuple((convert_value_to_qpanda2(item, task_id) for item in value))
    return clone_value(value)

def is_qiskit_quantum_circuit(value: Any) -> bool:
    return value.__class__.__name__ == 'QuantumCircuit' and hasattr(value, 'data') and hasattr(value, 'num_qubits')

def is_qiskit_operator_like(value: Any) -> bool:
    module = value.__class__.__module__
    return module.startswith('qiskit.') and value.__class__.__name__ != 'QuantumCircuit'

def qiskit_operator_matrix(value: Any) -> Any:
    import numpy as np
    from qiskit.quantum_info import Operator
    return np.asarray(Operator(value).data, dtype=complex)

def qiskit_circuit_to_cirq(circuit: Any, task_id: int) -> Any:
    import cirq
    import sympy
    qubits = cirq.LineQubit.range(circuit.num_qubits)
    converted = cirq.Circuit()
    for instruction in circuit.data:
        operation = instruction.operation
        qargs = [circuit.find_bit(qubit).index for qubit in instruction.qubits]
        cargs = [circuit.find_bit(clbit).index for clbit in instruction.clbits]
        name = operation.name.lower()
        if name == 'measure':
            converted.append(cirq.measure(qubits[qargs[0]], key=f'c{(cargs[0] if cargs else qargs[0])}'))
            continue
        gate = cirq_gate_for_qiskit_operation(operation, qargs, sympy)
        converted.append(gate.on(*(qubits[index] for index in qargs)))
    if task_id == 147 and (not converted.all_qubits()):
        converted.append(cirq.I.on_each(*qubits))
    return converted

def cirq_gate_for_qiskit_operation(operation: Any, qargs: list[int], sympy: Any) -> Any:
    import cirq
    import numpy as np
    name = operation.name.lower()
    params = list(getattr(operation, 'params', []) or [])
    if name == 'h':
        return cirq.H
    if name == 'x':
        return cirq.X
    if name == 'y':
        return cirq.Y
    if name == 'z':
        return cirq.Z
    if name == 's':
        return cirq.S
    if name == 'sdg':
        return cirq.S ** (-1)
    if name == 't':
        return cirq.T
    if name == 'tdg':
        return cirq.T ** (-1)
    if name in {'cx', 'cnot'}:
        return cirq.CNOT
    if name == 'cz':
        return cirq.CZ
    if name == 'swap':
        return cirq.SWAP
    if name == 'ccx':
        return cirq.CCX
    if name == 'rx':
        return cirq.rx(cirq_param(params[0], sympy))
    if name == 'ry':
        return cirq.ry(cirq_param(params[0], sympy))
    if name == 'rz':
        return cirq.rz(cirq_param(params[0], sympy))
    if name == 'p':
        return cirq.ZPowGate(exponent=cirq_param(params[0], sympy) / np.pi)
    if name == 'u':
        theta, phi, lam = [float(param) for param in params]
        return cirq.MatrixGate(operation.to_matrix())
    if hasattr(operation, 'to_matrix'):
        return cirq.MatrixGate(operation.to_matrix())
    raise TypeError(f'Unsupported Qiskit operation for Cirq conversion: {name}')

def cirq_param(value: Any, sympy: Any) -> Any:
    try:
        return float(value)
    except TypeError:
        return sympy.Symbol(getattr(value, 'name', str(value)))

def qiskit_circuit_to_qpanda(circuit: Any, task_id: int) -> Any:
    from pyqpanda3.core import CNOT, CZ, H, QCircuit, RX, RY, RZ, S, SWAP, T, X, Y, Z, measure
    converted = QCircuit(circuit.num_qubits)
    for instruction in circuit.data:
        operation = instruction.operation
        qargs = [circuit.find_bit(qubit).index for qubit in instruction.qubits]
        cargs = [circuit.find_bit(clbit).index for clbit in instruction.clbits]
        name = operation.name.lower()
        params = list(getattr(operation, 'params', []) or [])
        if name == 'measure':
            converted << measure(qargs[0], cargs[0] if cargs else qargs[0])
        elif name == 'h':
            converted << H(qargs[0])
        elif name == 'x':
            converted << X(qargs[0])
        elif name == 'y':
            converted << Y(qargs[0])
        elif name == 'z':
            converted << Z(qargs[0])
        elif name == 's':
            converted << S(qargs[0])
        elif name == 't':
            converted << T(qargs[0])
        elif name in {'cx', 'cnot'}:
            converted << CNOT(qargs[0], qargs[1])
        elif name == 'cz':
            converted << CZ(qargs[0], qargs[1])
        elif name == 'swap':
            converted << SWAP(qargs[0], qargs[1])
        elif name == 'rx':
            converted << RX(qargs[0], qpanda_angle(params[0]))
        elif name == 'ry':
            converted << RY(qargs[0], qpanda_angle(params[0]))
        elif name == 'rz':
            converted << RZ(qargs[0], qpanda_angle(params[0]))
        else:
            raise TypeError(f'Unsupported Qiskit operation for QPanda conversion: {name}')
    return converted

def qpanda_angle(value: Any) -> float:
    try:
        return float(value)
    except TypeError:
        return PARAMETER_VALUES[0]

def compare_outputs(reference: Any, candidate: Any) -> dict[str, Any]:
    is_sequence = isinstance(reference, (list, tuple)) or isinstance(candidate, (list, tuple))
    reference_items = normalize_output(reference)
    candidate_items = normalize_output(candidate)
    if len(reference_items) != len(candidate_items):
        raise ValueError(f'list length mismatch: reference={len(reference_items)}, candidate={len(candidate_items)}')
    item_metrics = [compare_one(ref_item, cand_item) for ref_item, cand_item in zip(reference_items, candidate_items)]
    return aggregate_item_metrics(item_metrics, is_sequence=is_sequence)

def compare_candidate_sequence_to_reference(candidate: Any, reference: Any) -> dict[str, Any]:
    candidate_items = normalize_sequence_output(candidate)
    if not candidate_items:
        raise ValueError('list length mismatch: reference>=1, candidate=0')
    item_metrics = [compare_one(reference, candidate_item) for candidate_item in candidate_items]
    return aggregate_item_metrics(item_metrics, is_sequence=True)

def normalize_output(value: Any) -> list[Any]:
    if isinstance(value, (list, tuple)):
        return list(value)
    return [value]

def normalize_sequence_output(value: Any) -> list[Any]:
    if not isinstance(value, (list, tuple)):
        raise TypeError(f'Expected list or tuple output, got {type(value).__name__}')
    return list(value)

def compare_one(reference: Any, candidate: Any) -> dict[str, float]:
    from qiskit.quantum_info import average_gate_fidelity, process_fidelity
    reference_prepared = bind_parameters(reference)
    expected_num_qubits = reference_num_qubits(reference_prepared)
    try:
        if is_qiskit_channel(reference_prepared):
            reference_op = reference_prepared
        else:
            reference_op = to_operator(reference_prepared)
    except Exception as exc:
        raise TypeError(f'reference output is not operator-like: {short_error(exc)}') from exc
    try:
        if is_qiskit_channel(reference_prepared):
            candidate_ops = to_channel_variants(candidate, reference_op, expected_num_qubits=expected_num_qubits)
        else:
            candidate_ops = to_operator_variants(candidate, expected_num_qubits=expected_num_qubits)
    except Exception as exc:
        raise TypeError(f'candidate output is not operator-like: {short_error(exc)}') from exc
    try:
        scored = [{'process_fidelity': float(process_fidelity(candidate_op, reference_op)), 'average_gate_fidelity': float(average_gate_fidelity(candidate_op, reference_op))} for candidate_op in candidate_ops]
    except Exception as exc:
        raise ValueError(f'candidate output has incompatible operator/channel semantics: {short_error(exc)}') from exc
    scored.sort(key=lambda item: (item['process_fidelity'], item['average_gate_fidelity']), reverse=True)
    return scored[0]

def reference_num_qubits(value: Any) -> int | None:
    num_qubits = object_num_qubits(value)
    if num_qubits is not None:
        return num_qubits
    for dims_attr in ('input_dims', 'output_dims'):
        dims_fn = getattr(value, dims_attr, None)
        if callable(dims_fn):
            try:
                dims = tuple(dims_fn())
            except Exception:
                continue
            if dims and all((dim == 2 for dim in dims)):
                return len(dims)
    data = getattr(value, 'data', None)
    if data is not None:
        return matrix_num_qubits(data)
    if is_matrix_like(value):
        return matrix_num_qubits(value)
    return None

def object_num_qubits(value: Any) -> int | None:
    if is_qiskit_quantum_circuit(value):
        return int(value.num_qubits)
    num_qubits = getattr(value, 'num_qubits', None)
    if isinstance(num_qubits, int):
        return num_qubits
    if callable(num_qubits):
        try:
            result = num_qubits()
        except TypeError:
            result = None
        if isinstance(result, int):
            return result
    qubits = getattr(value, 'qubits', None)
    if qubits is not None:
        try:
            return len(qubits)
        except TypeError:
            pass
    return None

def to_operator_variants(value: Any, *, expected_num_qubits: int | None=None) -> list[Any]:
    from qiskit.quantum_info import Operator
    prepared = bind_parameters(value)
    if is_cirq_circuit(prepared):
        return [Operator(unitary) for unitary in cirq_circuit_unitary_variants(prepared, expected_num_qubits)]
    if is_cirq_convertible(prepared):
        return [Operator(matrix) for matrix in cirq_value_unitary_variants(prepared, expected_num_qubits)]
    if is_qpanda_value(prepared):
        return [Operator(matrix) for matrix in matrix_order_variants(qpanda_matrix(prepared, expected_num_qubits), expected_num_qubits)]
    if is_matrix_like(prepared):
        return [Operator(matrix) for matrix in matrix_order_variants(prepared, expected_num_qubits)]
    return [to_operator(prepared)]

def to_channel_variants(value: Any, reference_channel: Any, *, expected_num_qubits: int | None=None) -> list[Any]:
    from qiskit.quantum_info import Choi, Operator
    prepared = bind_parameters(value)
    if is_qiskit_channel(prepared):
        return [prepared]
    if is_cirq_circuit(prepared):
        return [Operator(unitary) for unitary in cirq_circuit_unitary_variants(prepared, expected_num_qubits)]
    if is_cirq_convertible(prepared):
        return [Operator(matrix) for matrix in cirq_value_unitary_variants(prepared, expected_num_qubits)]
    if is_qpanda_value(prepared):
        return [Operator(matrix) for matrix in matrix_order_variants(qpanda_matrix(prepared, expected_num_qubits), expected_num_qubits)]
    if is_matrix_like(prepared):
        matrices = matrix_order_variants(prepared, expected_num_qubits)
        variants = []
        for matrix in matrices:
            if matrix.shape == getattr(reference_channel, 'data', ()).shape:
                variants.append(Choi(matrix))
            else:
                variants.append(Operator(matrix))
        return variants
    return [to_operator(prepared)]

def aggregate_item_metrics(item_metrics: list[dict[str, float]], *, is_sequence: bool) -> dict[str, Any]:
    if not item_metrics:
        raise ValueError('empty output sequence')
    min_pf = min((metric['process_fidelity'] for metric in item_metrics))
    min_agf = min((metric['average_gate_fidelity'] for metric in item_metrics))
    return {'process_fidelity': min_pf, 'average_gate_fidelity': min_agf, 'sequence_length': len(item_metrics) if is_sequence else None, 'item_metrics': item_metrics}

def process_metrics_pass(metrics: dict[str, Any]) -> bool:
    return metrics['process_fidelity'] >= PROCESS_FIDELITY_MIN and metrics['average_gate_fidelity'] >= AVERAGE_GATE_FIDELITY_MIN

def to_operator(value: Any) -> Any:
    import numpy as np
    from qiskit.circuit import Gate, Instruction, QuantumCircuit
    from qiskit.converters import dag_to_circuit
    from qiskit.dagcircuit import DAGCircuit
    from qiskit.quantum_info import Operator
    prepared = bind_parameters(value)
    if isinstance(prepared, DAGCircuit):
        prepared = dag_to_circuit(prepared)
    if isinstance(prepared, Operator):
        return prepared
    if isinstance(prepared, Gate):
        return Operator(prepared)
    if isinstance(prepared, Instruction):
        return Operator(prepared)
    if isinstance(prepared, QuantumCircuit):
        return Operator(strip_measurements(prepared))
    if is_cirq_convertible(prepared):
        return Operator(cirq_value_unitary_variants(prepared)[0])
    if is_qpanda_value(prepared):
        return Operator(qpanda_matrix(prepared))
    if isinstance(prepared, (int, float, complex)):
        return Operator([[prepared]])
    if hasattr(prepared, 'data') and prepared.__class__.__module__.startswith('qiskit.'):
        try:
            return Operator(prepared)
        except Exception:
            return Operator(np.asarray(prepared.data, dtype=complex))
    return Operator(prepared)

def is_cirq_value(value: Any) -> bool:
    return value.__class__.__module__.startswith('cirq')

def is_cirq_convertible(value: Any) -> bool:
    if is_cirq_value(value):
        return True
    try:
        import cirq
    except Exception:
        return False
    return isinstance(value, (cirq.Gate, cirq.Operation))

def is_cirq_circuit(value: Any) -> bool:
    return is_cirq_value(value) and value.__class__.__name__ == 'Circuit'

def cirq_value_unitary_variants(value: Any, expected_num_qubits: int | None=None) -> list[Any]:
    import cirq
    if is_cirq_circuit(value):
        return cirq_circuit_unitary_variants(value, expected_num_qubits)
    if expected_num_qubits is not None:
        if isinstance(value, cirq.Gate):
            qubits = cirq.LineQubit.range(value.num_qubits())
            return cirq_circuit_unitary_variants(cirq.Circuit(cirq.decompose(value.on(*qubits))), expected_num_qubits)
        if isinstance(value, cirq.Operation):
            return cirq_circuit_unitary_variants(cirq.Circuit(cirq.decompose(value)), expected_num_qubits)
    try:
        return matrix_order_variants(cirq.unitary(value), expected_num_qubits)
    except Exception as original_error:
        try:
            if isinstance(value, cirq.Gate):
                qubits = cirq.LineQubit.range(value.num_qubits())
                return cirq_circuit_unitary_variants(cirq.Circuit(cirq.decompose(value.on(*qubits))), expected_num_qubits)
            if isinstance(value, cirq.Operation):
                return cirq_circuit_unitary_variants(cirq.Circuit(cirq.decompose(value)), expected_num_qubits)
        except Exception:
            pass
        raise original_error

def cirq_circuit_unitary_variants(circuit: Any, expected_num_qubits: int | None=None) -> list[Any]:
    import cirq
    circuit = cirq.drop_terminal_measurements(circuit)
    qubits = sorted(circuit.all_qubits())
    if expected_num_qubits is not None and expected_num_qubits > len(qubits):
        expected_order = expected_cirq_qubit_order(qubits, expected_num_qubits)
        if expected_order is not None:
            qubits = expected_order
    if not qubits:
        return [circuit.unitary()]
    orders = [qubits, list(reversed(qubits))]
    variants = []
    seen: set[bytes] = set()
    for order in orders:
        unitary = circuit.unitary(qubit_order=order)
        marker = unitary.tobytes()
        if marker not in seen:
            seen.add(marker)
            variants.append(unitary)
    return variants

def expected_cirq_qubit_order(qubits: list[Any], expected_num_qubits: int) -> list[Any] | None:
    import cirq
    if not qubits or all((isinstance(qubit, cirq.LineQubit) for qubit in qubits)):
        expected_order = list(cirq.LineQubit.range(expected_num_qubits))
        if all((qubit in expected_order for qubit in qubits)):
            return expected_order
    if all((isinstance(qubit, cirq.NamedQubit) for qubit in qubits)):
        names = [qubit.name for qubit in qubits]
        bracket_matches = [re.fullmatch('(.+)\\[(\\d+)\\]', name) for name in names]
        if all((match is not None for match in bracket_matches)):
            prefixes = {match.group(1) for match in bracket_matches if match is not None}
            if len(prefixes) == 1:
                prefix = prefixes.pop()
                expected_order = [cirq.NamedQubit(f'{prefix}[{index}]') for index in range(expected_num_qubits)]
                if all((qubit in expected_order for qubit in qubits)):
                    return expected_order
        suffix_matches = [re.fullmatch('([A-Za-z_]+)(\\d+)', name) for name in names]
        if all((match is not None for match in suffix_matches)):
            prefixes = {match.group(1) for match in suffix_matches if match is not None}
            if len(prefixes) == 1:
                prefix = prefixes.pop()
                expected_order = [cirq.NamedQubit(f'{prefix}{index}') for index in range(expected_num_qubits)]
                if all((qubit in expected_order for qubit in qubits)):
                    return expected_order
    return None

def is_matrix_like(value: Any) -> bool:
    import numpy as np
    if isinstance(value, (str, bytes)):
        return False
    try:
        matrix = np.asarray(value)
    except Exception:
        return False
    return matrix.ndim == 2

def matrix_order_variants(value: Any, expected_num_qubits: int | None=None) -> list[Any]:
    import numpy as np
    matrix = np.asarray(value, dtype=complex)
    variants = []
    seen: set[tuple[tuple[int, ...], bytes]] = set()
    for base in expand_matrix_to_expected_qubits(matrix, expected_num_qubits):
        for candidate in (base, reverse_qubit_order_matrix(base)):
            if candidate is None:
                continue
            marker = (candidate.shape, candidate.tobytes())
            if marker not in seen:
                seen.add(marker)
                variants.append(candidate)
    return variants

def matrix_num_qubits(value: Any) -> int | None:
    import numpy as np
    try:
        matrix = np.asarray(value)
    except Exception:
        return None
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        return None
    dim = int(matrix.shape[0])
    if dim <= 0 or dim & dim - 1:
        return None
    num_qubits = int(math.log2(dim))
    return num_qubits if 2 ** num_qubits == dim else None

def expand_matrix_to_expected_qubits(matrix: Any, expected_num_qubits: int | None=None) -> list[Any]:
    import numpy as np
    matrix = np.asarray(matrix, dtype=complex)
    actual_num_qubits = matrix_num_qubits(matrix)
    if expected_num_qubits is None or actual_num_qubits is None or expected_num_qubits <= actual_num_qubits:
        return [matrix]
    idle_qubits = expected_num_qubits - actual_num_qubits
    identity = np.eye(2 ** idle_qubits, dtype=complex)
    expanded = [np.kron(matrix, identity)]
    right_expanded = np.kron(identity, matrix)
    if right_expanded.tobytes() != expanded[0].tobytes():
        expanded.append(right_expanded)
    return expanded

def reverse_qubit_order_matrix(matrix: Any) -> Any | None:
    import numpy as np
    matrix = np.asarray(matrix, dtype=complex)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        return None
    dim = matrix.shape[0]
    if dim == 0 or dim & dim - 1:
        return None
    num_qubits = int(math.log2(dim))
    if 2 ** num_qubits != dim or num_qubits <= 1:
        return None
    permutation = [reverse_bits(index, num_qubits) for index in range(dim)]
    return matrix[np.ix_(permutation, permutation)]

def reverse_bits(value: int, width: int) -> int:
    result = 0
    for _ in range(width):
        result = result << 1 | value & 1
        value >>= 1
    return result

def is_qiskit_channel(value: Any) -> bool:
    return any((cls.__name__ == 'QuantumChannel' and cls.__module__.startswith('qiskit.') for cls in value.__class__.__mro__))

def is_qpanda_value(value: Any) -> bool:
    return value.__class__.__module__.startswith('pyqpanda3') or is_qpanda2_value(value)

def is_qpanda2_value(value: Any) -> bool:
    qpanda2_type_names = {'QProg', 'QCircuit', 'QGate', 'QMeasure', 'ClassicalCondition', 'VariationalQuantumCircuit'}
    for cls in value.__class__.__mro__:
        module = getattr(cls, '__module__', '').lower()
        name = getattr(cls, '__name__', '')
        if module.startswith('pyqpanda3'):
            return False
        if module.startswith('pyqpanda'):
            return True
        if name in qpanda2_type_names and 'qpanda' in str(type(value)).lower():
            return True
    return False

def qpanda_matrix(value: Any, expected_num_qubits: int | None=None) -> Any:
    if is_qpanda2_value(value):
        return qpanda2_matrix(value, expected_num_qubits)
    if is_qpanda3_program_like(value):
        return qpanda3_program_matrix(value, expected_num_qubits)
    if hasattr(value, 'matrix'):
        matrix = value.matrix
        return matrix() if callable(matrix) else matrix
    raise TypeError(f'Cannot convert {type(value).__name__} to a matrix')

def is_qpanda3_program_like(value: Any) -> bool:
    return value.__class__.__module__.startswith('pyqpanda3') and value.__class__.__name__ in {'QProg', 'QCircuit'}

def qpanda3_program_matrix(value: Any, expected_num_qubits: int | None=None) -> Any:
    import numpy as np
    from pyqpanda3.core import CPUQVM, QProg, X
    program = value
    if value.__class__.__name__ == 'QCircuit':
        program = QProg()
        program << value
    if expected_num_qubits is None:
        expected_num_qubits = infer_qpanda3_program_num_qubits(program)
    if expected_num_qubits is None:
        raise TypeError(f'Cannot infer qubit count for {type(value).__name__}')
    if expected_num_qubits < 0:
        raise ValueError(f'Invalid qubit count: {expected_num_qubits}')
    dim = 2 ** expected_num_qubits
    matrix = np.empty((dim, dim), dtype=complex)
    for basis_index in range(dim):
        basis_program = QProg(expected_num_qubits)
        for qubit_index in range(expected_num_qubits):
            if basis_index >> qubit_index & 1:
                basis_program << X(qubit_index)
        basis_program << program
        state = run_qpanda3_statevector(basis_program)
        if state.size != dim:
            inferred = int(math.log2(state.size)) if state.size and state.size & state.size - 1 == 0 else 'unknown'
            raise ValueError(f'Expected {expected_num_qubits} qubits, got {inferred}')
        matrix[:, basis_index] = state
    return matrix

def infer_qpanda3_program_num_qubits(program: Any) -> int | None:
    state = run_qpanda3_statevector(program)
    dim = state.size
    if dim <= 0 or dim & dim - 1:
        return None
    return int(math.log2(dim))

def run_qpanda3_statevector(program: Any) -> Any:
    import numpy as np
    from pyqpanda3.core import CPUQVM
    qvm = CPUQVM()
    qvm.run(program, 1)
    result = qvm.result()
    return np.asarray(result.get_state_vector(), dtype=complex).reshape(-1)

def qpanda2_matrix(value: Any, expected_num_qubits: int | None=None) -> Any:
    import numpy as np
    import pyqpanda as pq
    prepared = value
    if hasattr(prepared, 'feed') and callable(prepared.feed):
        prepared = prepared.feed()
    try:
        flat = np.asarray(pq.get_matrix(prepared), dtype=complex).reshape(-1)
    except Exception as exc:
        raise TypeError(f'Cannot convert {type(value).__name__} to a qpanda2 matrix: {short_error(exc)}') from exc
    dim = int(round(math.sqrt(flat.size)))
    if dim * dim != flat.size:
        raise ValueError(f'qpanda2 matrix data is not square: {flat.size}')
    return flat.reshape((dim, dim))

def strip_measurements(circuit: Any) -> Any:
    if any((instruction.operation.name == 'measure' for instruction in circuit.data)):
        return circuit.remove_final_measurements(inplace=False)
    return circuit

def bind_parameters(value: Any) -> Any:
    parameters = sorted(getattr(value, 'parameters', []) or [], key=lambda item: item.name)
    if parameters:
        assignments = {parameter: PARAMETER_VALUES[index % len(PARAMETER_VALUES)] for index, parameter in enumerate(parameters)}
        if hasattr(value, 'assign_parameters'):
            return value.assign_parameters(assignments)
        if hasattr(value, 'bind_parameters'):
            return value.bind_parameters(assignments)
    if is_cirq_value(value):
        import cirq
        symbols = sorted(cirq.parameter_names(value))
        if symbols:
            resolver = {symbol: PARAMETER_VALUES[index % len(PARAMETER_VALUES)] for index, symbol in enumerate(symbols)}
            return cirq.resolve_parameters(value, resolver)
    return value

def resolve_code_path(root: Path, task_id: int) -> Path:
    root = root.expanduser().resolve()
    expected_name = f'code{task_id}.py'
    direct = root / expected_name
    if direct.is_file():
        return direct
    if root.is_file() and root.name == expected_name:
        return root
    if not root.exists():
        raise FileNotFoundError(root)
    matches = sorted((path for path in root.rglob(expected_name) if path.is_file() and '__pycache__' not in path.parts))
    if not matches:
        raise FileNotFoundError(f'{expected_name} not found under {root}')
    if len(matches) > 1:
        rendered = '\n  '.join((str(path) for path in matches))
        raise ValueError(f'multiple {expected_name} files found under {root}:\n  {rendered}')
    return matches[0]

def load_entry_function(path: Path, module_name: str, entrypoint: str) -> Callable[..., Any]:
    module = types.ModuleType(module_name)
    module.__file__ = str(path)
    module.__package__ = ''
    sys.modules[module_name] = module
    source = path.read_text(encoding='utf-8-sig')
    code = compile(source, str(path), 'exec')
    with prepend_sys_path(path.parent):
        exec(code, module.__dict__)
    value = vars(module).get(entrypoint)
    if value is None:
        public_functions = [name for name, candidate in vars(module).items() if inspect.isfunction(candidate) and candidate.__module__ == module.__name__ and (not name.startswith('_'))]
        raise ValueError(f'Missing required function {entrypoint!r}. Public functions found: {public_functions}')
    if not inspect.isfunction(value):
        raise TypeError(f'{entrypoint!r} in {path} is not a function')
    value.__eval_source_path__ = str(path)
    value.__eval_module_name__ = module_name
    value.__eval_entrypoint__ = entrypoint
    return value

class DeferredEntryFunction:

    def __init__(self, path: Path, module_name: str, entrypoint: str) -> None:
        self.__eval_source_path__ = str(path)
        self.__eval_module_name__ = module_name
        self.__eval_entrypoint__ = entrypoint

@contextmanager
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

def call_and_capture(func: Callable[..., Any], args: tuple[Any, ...], kwargs: dict[str, Any]) -> dict[str, Any]:
    try:
        return {'value': func(*args, **kwargs), 'args': args, 'kwargs': kwargs, 'error': None}
    except Exception as exc:
        return {'value': None, 'args': args, 'kwargs': kwargs, 'error': short_error(exc)}

def call_framework_candidate(func: Callable[..., Any], framework: str, args: tuple[Any, ...], kwargs: dict[str, Any], timeout_seconds: float=QPANDA2_CALL_TIMEOUT_SECONDS) -> dict[str, Any]:
    if framework == 'qpanda2':
        return call_qpanda2_candidate_subprocess(func, args, kwargs, timeout_seconds)
    if framework == 'pennylane':
        return call_pennylane_candidate_subprocess(func, args, kwargs, timeout_seconds)
    return call_and_capture(func, args, kwargs)

def call_pennylane_candidate_subprocess(func: Callable[..., Any], args: tuple[Any, ...], kwargs: dict[str, Any], timeout_seconds: float=QPANDA2_CALL_TIMEOUT_SECONDS) -> dict[str, Any]:
    source_path = getattr(func, '__eval_source_path__', None)
    module_name = getattr(func, '__eval_module_name__', None)
    entrypoint = getattr(func, '__eval_entrypoint__', None)
    if not source_path or not module_name or (not entrypoint):
        return {'value': None, 'args': args, 'kwargs': kwargs, 'error': 'INTERNAL ERROR: function lacks eval metadata', 'error_type': 'evaluator_metadata_error'}
    result_file = tempfile.NamedTemporaryFile(prefix='class3_pennylane_', suffix='.pkl', delete=False)
    result_path = result_file.name
    result_file.close()
    process = mp.Process(target=pennylane_candidate_worker, args=(result_path, source_path, module_name, entrypoint, args, kwargs))
    try:
        process.start()
        process.join(timeout_seconds)
        if process.is_alive():
            process.terminate()
            process.join(5)
            if process.is_alive():
                process.kill()
                process.join()
            return {'value': None, 'args': args, 'kwargs': kwargs, 'error': f'TIMEOUT after {timeout_seconds:g}s', 'error_type': 'timeout_or_resource_limit'}
        if Path(result_path).stat().st_size > 0:
            with open(result_path, 'rb') as handle:
                try:
                    return pickle.load(handle)
                except Exception as exc:
                    return {'value': None, 'args': args, 'kwargs': kwargs, 'error': f'PennyLane evaluator could not deserialize worker output: {short_error(exc)}', 'error_type': 'evaluator_deserialization_error'}
        if process.exitcode not in (0, None):
            return {'value': None, 'args': args, 'kwargs': kwargs, 'error': f'PROCESS EXITED with code {process.exitcode}', 'error_type': 'evaluator_process_error'}
        return {'value': None, 'args': args, 'kwargs': kwargs, 'error': 'PROCESS EXITED without result', 'error_type': 'evaluator_process_error'}
    except Exception as exc:
        return {'value': None, 'args': args, 'kwargs': kwargs, 'error': f'PennyLane evaluator process failed: {short_error(exc)}', 'error_type': 'evaluator_process_error'}
    finally:
        try:
            Path(result_path).unlink()
        except FileNotFoundError:
            pass

def pennylane_candidate_worker(result_path: str, source_path: str, module_name: str, entrypoint: str, args: tuple[Any, ...], kwargs: dict[str, Any]) -> None:
    try:
        func = load_entry_function(Path(source_path), module_name, entrypoint)
    except Exception as exc:
        result = {'value': None, 'args': args, 'kwargs': kwargs, 'error': short_error(exc), 'error_type': 'candidate_setup_or_environment_error'}
    else:
        try:
            value = func(*args, **kwargs)
        except Exception as exc:
            result = {'value': None, 'args': args, 'kwargs': kwargs, 'error': short_error(exc), 'error_type': 'unclassified_candidate_execution_error'}
        else:
            try:
                if value is None and is_pennylane_worker_callable(func):
                    value = pennylane_callable_to_worker_script(func, args, kwargs)
                else:
                    value = normalize_pennylane_worker_value(value, args, kwargs)
            except Exception as exc:
                result = {'value': None, 'args': args, 'kwargs': kwargs, 'error': short_error(exc), 'error_type': 'normalization_or_candidate_reexecution_error'}
            else:
                result = {'value': value, 'args': args, 'kwargs': kwargs, 'error': None, 'error_type': None}
    try:
        with open(result_path, 'wb') as handle:
            pickle.dump(result, handle)
    except Exception as exc:
        with open(result_path, 'wb') as handle:
            pickle.dump({'value': None, 'args': safe_repr(args), 'kwargs': safe_repr(kwargs), 'error': f'PennyLane worker could not serialize its result: {short_error(exc)}', 'error_type': 'evaluator_serialization_error'}, handle)

def normalize_pennylane_worker_value(value: Any, args: tuple[Any, ...], kwargs: dict[str, Any]) -> Any:
    module_name = getattr(value.__class__, '__module__', '')
    if module_name.startswith('pennylane') and hasattr(value, 'operations') and hasattr(value, 'measurements'):
        return value
    if isinstance(value, list):
        return [normalize_pennylane_worker_value(item, args, kwargs) for item in value]
    if isinstance(value, tuple):
        return tuple((normalize_pennylane_worker_value(item, args, kwargs) for item in value))
    if isinstance(value, dict):
        return {key: normalize_pennylane_worker_value(item, args, kwargs) for key, item in value.items()}
    try:
        import pennylane as qml
    except Exception:
        return value
    if isinstance(value, qml.QNode):
        function = getattr(value, 'func', None)
        if not callable(function):
            raise TypeError('PennyLane QNode has no callable quantum function')
        script_args, script_kwargs = build_pennylane_worker_args(function)
        script = qml.tape.make_qscript(function)(*script_args, **script_kwargs)
        apply_pennylane_worker_metadata(script, value)
        return script
    if is_pennylane_worker_callable(value):
        return pennylane_callable_to_worker_script(value, args, kwargs)
    return value

def is_pennylane_worker_callable(value: Any) -> bool:
    if not callable(value) or isinstance(value, type):
        return False
    globals_dict = getattr(value, '__globals__', {})
    return any((getattr(module, '__name__', '') == 'pennylane' for module in globals_dict.values()))

def pennylane_callable_to_worker_script(value: Any, args: tuple[Any, ...], kwargs: dict[str, Any]) -> Any:
    import pennylane as qml
    script = qml.tape.make_qscript(value)(*args, **kwargs)
    apply_pennylane_worker_metadata(script, value)
    return script

def build_pennylane_worker_args(function: Callable[..., Any]) -> tuple[tuple[Any, ...], dict[str, Any]]:
    positional: list[Any] = []
    keyword: dict[str, Any] = {}
    next_value = 0
    for parameter in inspect.signature(function).parameters.values():
        if parameter.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            continue
        if parameter.default is not inspect._empty and parameter.default is not None:
            continue
        assigned = PARAMETER_VALUES[next_value % len(PARAMETER_VALUES)]
        next_value += 1
        if parameter.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD):
            positional.append(assigned)
        else:
            keyword[parameter.name] = assigned
    return (tuple(positional), keyword)

def apply_pennylane_worker_metadata(script: Any, source: Any) -> None:
    import pennylane as qml
    device = getattr(source, 'device', None)
    wires = list(getattr(script, 'wires', []) or [])
    if device is not None:
        wires = list(getattr(device, 'wires', []) or wires)
        if not wires:
            num_wires = getattr(device, 'num_wires', None)
            if num_wires:
                wires = list(range(int(num_wires)))
    if wires:
        if all((isinstance(wire, int) and wire >= 0 for wire in wires)):
            wires = list(range(max(wires) + 1))
        script.declared_wires = qml.wires.Wires(wires)
        script.num_qubits = len(wires)
    elif not hasattr(script, 'num_qubits'):
        script.num_qubits = 0
    if not hasattr(script, 'num_clbits'):
        script.num_clbits = 0
    if not hasattr(script, 'classical_bits'):
        script.classical_bits = []

def call_qpanda2_candidate_subprocess(func: Callable[..., Any], args: tuple[Any, ...], kwargs: dict[str, Any], timeout_seconds: float=QPANDA2_CALL_TIMEOUT_SECONDS) -> dict[str, Any]:
    source_path = getattr(func, '__eval_source_path__', None)
    module_name = getattr(func, '__eval_module_name__', None)
    entrypoint = getattr(func, '__eval_entrypoint__', None)
    if not source_path or not module_name or (not entrypoint):
        return {'value': None, 'args': args, 'kwargs': kwargs, 'error': 'INTERNAL ERROR: function lacks eval metadata'}
    result_file = tempfile.NamedTemporaryFile(prefix='class3_qpanda2_', suffix='.pkl', delete=False)
    result_path = result_file.name
    result_file.close()
    process = mp.Process(target=qpanda2_candidate_worker, args=(result_path, source_path, module_name, entrypoint, args, kwargs))
    process.start()
    process.join(timeout_seconds)
    try:
        if process.is_alive():
            process.terminate()
            process.join(5)
            if process.is_alive():
                process.kill()
                process.join()
            return {'value': None, 'args': args, 'kwargs': kwargs, 'error': f'TIMEOUT after {timeout_seconds:g}s'}
        if Path(result_path).stat().st_size > 0:
            with open(result_path, 'rb') as handle:
                try:
                    return pickle.load(handle)
                except Exception as exc:
                    return {'value': None, 'args': args, 'kwargs': kwargs, 'error': f'candidate produced non-deserializable qpanda2 result: {short_error(exc)}'}
        if process.exitcode not in (0, None):
            return {'value': None, 'args': args, 'kwargs': kwargs, 'error': f'PROCESS EXITED with code {process.exitcode}'}
        return {'value': None, 'args': args, 'kwargs': kwargs, 'error': 'PROCESS EXITED without result'}
    finally:
        try:
            Path(result_path).unlink()
        except FileNotFoundError:
            pass

def qpanda2_candidate_worker(result_path: str, source_path: str, module_name: str, entrypoint: str, args: tuple[Any, ...], kwargs: dict[str, Any]) -> None:
    try:
        func = load_entry_function(Path(source_path), module_name, entrypoint)
        value = func(*args, **kwargs)
        result = {'value': serialize_qpanda2_worker_value(value, strict=True), 'args': serialize_qpanda2_worker_value(args, strict=False), 'kwargs': serialize_qpanda2_worker_value(kwargs, strict=False), 'error': None}
    except Exception as exc:
        result = {'value': None, 'args': serialize_qpanda2_worker_value(args, strict=False), 'kwargs': serialize_qpanda2_worker_value(kwargs, strict=False), 'error': short_error(exc)}
    with open(result_path, 'wb') as handle:
        try:
            pickle.dump(result, handle)
        except Exception as exc:
            fallback = {'value': None, 'args': safe_repr(args), 'kwargs': safe_repr(kwargs), 'error': f'candidate produced non-serializable qpanda2 result: {short_error(exc)}'}
            pickle.dump(fallback, handle)

def serialize_qpanda2_worker_value(value: Any, *, strict: bool) -> Any:
    if is_qpanda2_value(value):
        try:
            return qpanda2_matrix(value)
        except Exception as exc:
            if strict:
                raise TypeError(f'candidate returned qpanda2 {type(value).__name__} that cannot be converted to matrix: {short_error(exc)}') from exc
            return f'<qpanda2 {type(value).__name__}: {short_error(exc)}>'
    if isinstance(value, dict):
        return {key: serialize_qpanda2_worker_value(item, strict=strict) for key, item in value.items()}
    if isinstance(value, list):
        return [serialize_qpanda2_worker_value(item, strict=strict) for item in value]
    if isinstance(value, tuple):
        return tuple((serialize_qpanda2_worker_value(item, strict=strict) for item in value))
    module_name = getattr(value.__class__, '__module__', '')
    if module_name.startswith('class3_'):
        if strict:
            raise TypeError(f'candidate returned unsupported custom object {type(value).__name__}')
        return safe_repr(value)
    try:
        pickle.dumps(value)
    except Exception as exc:
        if strict:
            raise TypeError(f'candidate returned unsupported non-serializable {type(value).__name__}; expected a matrix/operator-like qpanda2 result') from exc
        return safe_repr(value)
    return value

def safe_repr(value: Any) -> str:
    try:
        rendered = repr(value)
    except Exception:
        rendered = f'<unrepresentable {type(value).__name__}>'
    return rendered[:500]

def clone_value(value: Any) -> Any:
    try:
        return copy.deepcopy(value)
    except Exception:
        return value

def short_error(exc: BaseException) -> str:
    message = str(exc).strip()
    if not message:
        message = exc.__class__.__name__
    return message.splitlines()[0][:300]

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
    return {'mode': 'cross_language_translate', 'class_id': 3, 'model': model, 'framework': framework, 'dir_a': str(std_dir), 'dir_b': str(candidate_dir), 'thresholds': thresholds(), 'environment': build_environment_info(), 'summary': {}, 'results': results}

def task_pass_metrics(samples: list[dict[str, Any]]) -> tuple[int, float | None, float | None, float | None]:
    sample_passes = [bool(sample.get('sample_pass')) for sample in samples]
    pass_count = sum((1 for passed in sample_passes if passed))
    if any((sample.get('sample_status', infer_sample_status(sample)) == 'ERROR' for sample in samples)):
        return (pass_count, None, None, None)
    return (pass_count, estimate_pass_at_k(len(sample_passes), pass_count, 1), estimate_pass_at_k(len(sample_passes), pass_count, 3), estimate_pass_at_k(len(sample_passes), pass_count, 5))

def estimate_pass_at_k(sample_count: int, pass_count: int, k: int) -> float | None:
    if sample_count <= 0 or k <= 0 or sample_count < k:
        return None
    if pass_count <= 0:
        return 0.0
    if sample_count - pass_count < k:
        return 1.0
    return 1.0 - math.comb(sample_count - pass_count, k) / math.comb(sample_count, k)

def write_report_bundle(report_dir: Path, details: dict[str, Any]) -> None:
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
    write_flat_results(report_dir, flatten_results(str(details.get('model')), details))
    write_metrics_xlsx(report_dir / 'metrics.xlsx', details)

def build_text_report(details: dict[str, Any]) -> str:
    rows = []
    for result in details.get('results', []) or []:
        code = f'code{result['task_id']}'
        rows.append([code, str(result.get('sample_count') or 0), str(result.get('pass_count') or 0), format_metric(result.get('pass_at_1')), format_metric(result.get('pass_at_3')), format_metric(result.get('pass_at_5')), build_task_note(result)])
    headers = ['code', 'samples', 'c', 'pass@1', 'pass@3', 'pass@5', 'note']
    table = format_table(headers, rows)
    t = details.get('thresholds', {})
    summary = details.get('summary', {})
    return '\n'.join(['Cross-language Class 3 translation evaluation report', f'model: {details.get('model')}', f'framework: {details.get('framework')}', f'dir_a: {details.get('dir_a')}', f'dir_b: {details.get('dir_b')}', f'thresholds: process_fidelity >= {t.get('process_fidelity_min')}, average_gate_fidelity >= {t.get('average_gate_fidelity_min')}', '', table, '', 'overall summary:', f'task_RAW_PASS: {summary.get('task_RAW_PASS', 0)} / {summary.get('task_total', 0)}', f'task_FAIL: {summary.get('task_FAIL', 0)} / {summary.get('task_total', 0)}', f'task_ERROR: {summary.get('task_ERROR', 0)} / {summary.get('task_total', 0)}', f'sample_PASS: {summary.get('sample_PASS', 0)} / {summary.get('sample_total', 0)}', f'sample_FAIL: {summary.get('sample_FAIL', 0)} / {summary.get('sample_total', 0)}', f'sample_ERROR: {summary.get('sample_ERROR', 0)} / {summary.get('sample_total', 0)}', f'pass@1: {format_rate(summary.get('pass_at_1'))}', f'pass@3: {format_rate(summary.get('pass_at_3'))}', f'pass@5: {format_rate(summary.get('pass_at_5'))}', f'pass@k defined tasks: @1={summary.get('pass_at_1_defined_task_count', 0)}, @3={summary.get('pass_at_3_defined_task_count', 0)}, @5={summary.get('pass_at_k_defined_task_count', 0)}', ''])

def build_classification_rows(details: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for result in details.get('results', []) or []:
        final_label = 'PASS' if int(result.get('pass_count') or 0) > 0 else 'FAIL'
        rows.append({'task_id': result.get('task_id'), 'class_id': result.get('class_id'), 'framework': details.get('framework'), 'function': result.get('function'), 'path_b': result.get('best_sample_path') or result.get('path_b'), 'raw_label': result.get('raw_label'), 'raw_status': result.get('raw_status'), 'final_label': final_label, 'decision_stage': 'pass@5', 'passed': final_label == 'PASS', 'sample_count': result.get('sample_count'), 'pass_count': result.get('pass_count'), 'pass_at_1': result.get('pass_at_1'), 'pass_at_3': result.get('pass_at_3'), 'pass_at_5': result.get('pass_at_5'), 'best_sample_index': result.get('best_sample_index'), 'best_sample_path': result.get('best_sample_path'), 'sample_statuses': sample_statuses(result), 'failure_note': None if final_label == 'PASS' else 'evaluation incomplete; result is undetermined' if final_label == 'ERROR' else 'all samples failed', 'error_summary': build_error_summary(result)})
    return rows

def sample_statuses(result: dict[str, Any]) -> list[dict[str, Any]]:
    statuses = []
    for sample in result.get('samples', []) or []:
        statuses.append({'sample_index': sample.get('sample_index'), 'candidate_path': sample.get('candidate_path'), 'status': sample.get('sample_status', infer_sample_status(sample)), 'label': sample.get('sample_label'), 'cases': [{'label': case.get('label'), 'status': case.get('status'), 'process_fidelity': case.get('process_fidelity'), 'average_gate_fidelity': case.get('average_gate_fidelity'), 'sequence_length': case.get('sequence_length')} for case in sample.get('cases', []) or []]})
    return statuses

def build_error_summary(result: dict[str, Any]) -> dict[str, Any]:
    errors: list[dict[str, str]] = []
    for sample in result.get('samples', []) or []:
        setup_error = sample.get('setup_error')
        if setup_error:
            errors.append({'sample_index': sample.get('sample_index'), 'case': 'SETUP', 'error': setup_error})
        for case in sample.get('cases', []) or []:
            error = case.get('error')
            if error:
                errors.append({'sample_index': sample.get('sample_index'), 'case': str(case.get('label')), 'error': str(error)})
    return {'raw': errors} if errors else {}

def build_fail_samples(rows: list[dict[str, Any]], details: dict[str, Any]) -> list[dict[str, Any]]:
    by_task = {int(result['task_id']): result for result in details['results']}
    return [{'task_id': row['task_id'], 'class_id': row.get('class_id'), 'framework': row.get('framework'), 'function': row.get('function'), 'path_b': row.get('path_b'), 'failure_note': row.get('failure_note'), 'raw': by_task.get(int(row['task_id']))} for row in rows if row.get('final_label') == 'FAIL']

def build_error_samples(rows: list[dict[str, Any]], details: dict[str, Any]) -> list[dict[str, Any]]:
    by_task = {int(result['task_id']): result for result in details['results']}
    return [{'task_id': row['task_id'], 'class_id': row.get('class_id'), 'framework': row.get('framework'), 'function': row.get('function'), 'path_b': row.get('path_b'), 'failure_note': row.get('failure_note'), 'raw': by_task.get(int(row['task_id']))} for row in rows if row.get('final_label') == 'ERROR']

def build_summary(classification: list[dict[str, Any]]) -> dict[str, Any]:
    task_total = len(classification)
    task_raw_pass = sum((1 for row in classification if int(row.get('pass_count') or 0) > 0))
    task_error = sum((1 for row in classification if row.get('raw_status') == 'ERROR'))
    sample_total = sum((int(row.get('sample_count') or 0) for row in classification))
    sample_pass = sum((int(row.get('pass_count') or 0) for row in classification))
    all_sample_statuses = [status for row in classification for status in row.get('sample_statuses') or []]
    sample_error = sum((1 for item in all_sample_statuses if item.get('status') == 'ERROR'))
    sample_fail = sum((1 for item in all_sample_statuses if item.get('status') == 'FAIL'))
    pass_at_1_values = [float(row['pass_at_1']) for row in classification if row.get('pass_at_1') is not None]
    pass_at_3_values = [float(row['pass_at_3']) for row in classification if row.get('pass_at_3') is not None]
    pass_at_5_values = [float(row['pass_at_5']) for row in classification if row.get('pass_at_5') is not None]
    pass_at_1_sum = sum(pass_at_1_values)
    pass_at_3_sum = sum(pass_at_3_values)
    pass_at_5_sum = sum(pass_at_5_values)
    return {'task_total': task_total, 'task_RAW_PASS': task_raw_pass, 'task_FAIL': sum((1 for row in classification if row.get('raw_status') == 'FAIL')), 'task_ERROR': task_error, 'sample_total': sample_total, 'sample_PASS': sample_pass, 'sample_FAIL': sample_fail, 'sample_ERROR': sample_error, 'pass_at_1_sum': pass_at_1_sum, 'pass_at_3_sum': pass_at_3_sum, 'pass_at_5_sum': pass_at_5_sum, 'pass_at_1': None if not pass_at_1_values else pass_at_1_sum / len(pass_at_1_values), 'pass_at_3': None if not pass_at_3_values else pass_at_3_sum / len(pass_at_3_values), 'pass_at_5': None if not pass_at_5_values else pass_at_5_sum / len(pass_at_5_values), 'pass_at_1_defined_task_count': len(pass_at_1_values), 'pass_at_3_defined_task_count': len(pass_at_3_values), 'pass_at_k_defined_task_count': len(pass_at_5_values)}

def build_environment_report(info: dict[str, Any] | None=None) -> str:
    env = info or build_environment_info()
    lines = ['Cross-language Class 3 translation evaluation environment', f'python: {env.get('python')}', f'platform: {env.get('platform')}']
    for package, version in env.get('packages', {}).items():
        lines.append(f'{package}: {version or 'not installed'}')
    return '\n'.join(lines) + '\n'

def build_environment_info() -> dict[str, Any]:
    info: dict[str, Any] = {'python': platform.python_version(), 'platform': platform.platform(), 'packages': {}}
    for package in ('qiskit', 'qiskit-aer', 'qiskit-ibm-runtime', 'cirq', 'pyqpanda3', 'numpy'):
        try:
            version = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            version = None
        info['packages'][package] = version
    return info

def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8', newline='\n')

def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='\n') as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + '\n')

def write_summary_csv(path: Path, summary: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ['metric,value']
    for key, value in build_summary_csv_rows(summary):
        lines.append(f'{key},{value}')
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8', newline='\n')

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

def first_line(value: str | None) -> str:
    if not value:
        return ''
    return str(value).strip().splitlines()[0][:300]

def flatten_results(model: str, details: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    framework = details.get('framework')
    for result in details.get('results', []) or []:
        for sample in result.get('samples', []) or []:
            if sample.get('setup_error'):
                rows.append({'model': model, 'framework': framework, 'task_id': result.get('task_id'), 'function': result.get('function'), 'sample_index': sample.get('sample_index'), 'candidate_path': sample.get('candidate_path'), 'case': 'SETUP', 'status': 'FAIL', 'raw_label': sample.get('sample_label'), 'error': sample.get('setup_error')})
                continue
            for case in sample.get('cases', []) or []:
                rows.append({'model': model, 'framework': framework, 'task_id': result.get('task_id'), 'function': result.get('function'), 'sample_index': sample.get('sample_index'), 'candidate_path': sample.get('candidate_path'), 'case': case.get('label'), 'status': case.get('status'), 'raw_label': sample.get('sample_label'), 'process_fidelity': case.get('process_fidelity'), 'average_gate_fidelity': case.get('average_gate_fidelity'), 'sequence_length': case.get('sequence_length'), 'error': case.get('error')})
    return rows

def write_flat_results(report_root: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames = ['model', 'framework', 'task_id', 'function', 'sample_index', 'candidate_path', 'case', 'status', 'raw_label', 'process_fidelity', 'average_gate_fidelity', 'sequence_length', 'error']
    report_root.mkdir(parents=True, exist_ok=True)
    with (report_root / 'results.csv').open('w', encoding='utf-8-sig', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, '') for key in fieldnames})
    write_jsonl(report_root / 'results.jsonl', rows)

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
    headers = ['model', 'framework', 'code', 'task_id', 'function', 'sample_index', 'candidate_file', 'sample_pass', 'sample_status', 'case_count', 'pass_case_count', 'fail_case_count', 'error_case_count', 'min_process_fidelity', 'min_average_gate_fidelity', 'process_fidelity_threshold', 'average_gate_fidelity_threshold', 'note']
    thresholds = details.get('thresholds') or {}
    rows = []
    for result in details.get('results', []) or []:
        for sample in result.get('samples', []) or []:
            cases = sample.get('cases', []) or []
            pass_case_count = sum((1 for case in cases if case.get('status') == 'PASS'))
            fail_case_count = sum((1 for case in cases if case.get('status') == 'FAIL'))
            error_case_count = sum((1 for case in cases if case.get('status') == 'ERROR'))
            process_fidelities = [case.get('process_fidelity') for case in cases if case.get('process_fidelity') is not None]
            average_gate_fidelities = [case.get('average_gate_fidelity') for case in cases if case.get('average_gate_fidelity') is not None]
            notes = [first_line(sample.get('setup_error'))] if sample.get('setup_error') else []
            notes.extend((first_line(case.get('error')) for case in cases if case.get('error')))
            note = '; '.join(notes)
            rows.append([details.get('model'), details.get('framework'), f'code{result.get('task_id')}', result.get('task_id'), result.get('function'), sample.get('sample_index'), Path(str(sample.get('candidate_path') or '')).name, bool(sample.get('sample_pass')), sample.get('sample_status', infer_sample_status(sample)), len(cases), pass_case_count, fail_case_count, error_case_count, min(process_fidelities) if process_fidelities else None, min(average_gate_fidelities) if average_gate_fidelities else None, thresholds.get('process_fidelity_min'), thresholds.get('average_gate_fidelity_min'), first_line(note)])
    return (headers, rows)

def build_metrics_case_rows(details: dict[str, Any]) -> tuple[list[str], list[list[Any]]]:
    headers = ['model', 'framework', 'code', 'task_id', 'function', 'sample_index', 'case', 'status', 'process_fidelity', 'process_fidelity_threshold', 'process_fidelity_pass', 'average_gate_fidelity', 'average_gate_fidelity_threshold', 'average_gate_fidelity_pass', 'sequence_length', 'error', 'candidate_path']
    thresholds = details.get('thresholds') or {}
    process_threshold = thresholds.get('process_fidelity_min')
    average_threshold = thresholds.get('average_gate_fidelity_min')
    rows = []
    for result in details.get('results', []) or []:
        for sample in result.get('samples', []) or []:
            for case in sample.get('cases', []) or []:
                process_fidelity = case.get('process_fidelity')
                average_gate_fidelity = case.get('average_gate_fidelity')
                rows.append([details.get('model'), details.get('framework'), f'code{result.get('task_id')}', result.get('task_id'), result.get('function'), sample.get('sample_index'), case.get('label'), case.get('status'), process_fidelity, process_threshold, None if process_fidelity is None else process_fidelity >= process_threshold, average_gate_fidelity, average_threshold, None if average_gate_fidelity is None else average_gate_fidelity >= average_threshold, case.get('sequence_length'), case.get('error'), sample.get('candidate_path')])
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

def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8', newline='\n')

def format_metric(value: Any) -> str:
    if value is None:
        return '-'
    number = float(value)
    if math.isnan(number):
        return 'nan'
    return f'{number:.12g}'
