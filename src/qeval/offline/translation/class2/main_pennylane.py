import argparse
import contextlib
import importlib.metadata
import io
import math
import multiprocessing as mp
import pickle
import platform
import tempfile
import traceback
from pathlib import Path
from typing import Any, Callable
import numpy as np
from main import CASE_TIMEOUT_SECONDS, CIRCUIT_STATE_TASKS, DEFAULT_REPORT_DIR, STATE_TASKS, as_density_matrix, aggregate_task_status, base_case_row, best_quantum_state_comparison, call_and_capture, clone_value, combine_errors, compare_quantum_states, coerce_pair, candidate_path_for_sample, discover_candidate_samples, flatten_results, format_outcome_error, load_entry_function, parse_task_ids, reconstruct_schmidt_state, resolve_models, reverse_bits, state_metrics_pass, std_path, task_pass_metrics, thresholds, write_flat_results, write_report_bundle
from tasks import build_qiskit_cases, get_task_spec
FRAMEWORK = 'pennylane'
FRAMEWORKS = (FRAMEWORK,)
PENNYLANE_BUNDLE_KEY = '__pennylane_bundle__'

class PennyLaneEvaluatorSerializationError(RuntimeError):
    pass
PENNYLANE_ARTIFACT_KEY = '__pennylane_artifact__'

def parse_frameworks(raw: str) -> list[str]:
    frameworks = [part.strip().lower() for part in raw.split(',') if part.strip()]
    if not frameworks:
        raise ValueError('At least one framework is required.')
    unsupported = sorted(set(frameworks).difference(FRAMEWORKS))
    if unsupported:
        raise ValueError(f'Unsupported framework(s): {unsupported}')
    return frameworks

def pennylane_bell_circuit() -> None:
    import pennylane as qml
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0, 1])

def build_pennylane_cases() -> dict[int, list[dict[str, Any]]]:
    from qiskit.quantum_info import random_statevector
    schmidt_data = np.asarray(random_statevector(4, seed=42).data, dtype=complex)
    epsilon_0_1 = 0.1
    mutual_information_threshold = 0.5
    return {2: [{'label': 'default', 'args': ()}], 3: [{'label': 'drawing_false', 'args': (False,)}], 5: [{'label': 'default', 'args': ()}], 6: [{'label': 'num_qubits_3', 'args': (3,)}], 11: [{'label': 'bell_state', 'args': (pennylane_bell_circuit,)}], 39: [{'label': 'n3', 'args': (3,)}], 62: [{'label': 'z_one', 'args': ([1], [0])}, {'label': 'x_zero', 'args': ([0], [1])}, {'label': 'mixed_four_qubits', 'args': ([0, 1, 1, 0], [0, 0, 1, 1])}], 66: [{'label': 'default', 'args': ()}], 83: [{'label': 'default', 'args': ()}], 136: [{'label': 'epsilon_0_1', 'args': (epsilon_0_1,)}], 137: [{'label': 'epsilon_0_1', 'args': (epsilon_0_1,)}], 138: [{'label': 'epsilon_0_5', 'args': (mutual_information_threshold,)}], 139: [{'label': 'random_state_seed_42_qargs_1', 'args': (schmidt_data, [1])}], 142: [{'label': 'default', 'args': ()}], 143: [{'label': 'default', 'args': ()}], 144: [{'label': 'default', 'args': ()}]}

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
            results = []
            for task_id in task_ids:
                sample_paths = discover_candidate_samples(output_dir, model, framework, task_id)
                if not sample_paths:
                    sample_paths = [(1, candidate_path_for_sample(output_dir, model, framework, task_id, 1))]
                for sample_index, candidate_path in sample_paths:
                    results.append(evaluate_task(task_id, std_dir, candidate_dir, sample_index, candidate_path))
            details = build_raw_details(results, std_dir, candidate_dir, model, framework)
            model_report_dir = report_root / model / framework
            write_report_bundle(model_report_dir, details)
            flat_rows.extend(flatten_results(model, details))
    if flat_rows:
        write_flat_results(report_root, flat_rows)
    return 0

def evaluate_task(task_id: int, std_dir: Path, candidate_dir: Path, sample_index: int=1, candidate_path: Path | None=None) -> dict[str, Any]:
    spec = get_task_spec(task_id)
    candidate_path = candidate_path or candidate_dir / f'code{task_id}.py'
    result: dict[str, Any] = {'task_id': task_id, 'class_id': spec.class_id, 'path_a': str(std_path(std_dir, task_id)), 'path_b': str(candidate_path), 'candidate_path': str(candidate_path), 'sample_index': sample_index, 'framework': FRAMEWORK, 'function': spec.entrypoint, 'cases': [], 'sample_pass': False, 'sample_status': 'FAIL', 'sample_label': 'FAIL', 'raw_status': 'FAIL', 'raw_label': 'FAIL', 'setup_error': None}
    try:
        func_b = load_entry_function(candidate_path, f'{FRAMEWORK}_b_code{task_id}_s{sample_index}', spec.entrypoint)
        func_a = None
        if task_id in STATE_TASKS or task_id in CIRCUIT_STATE_TASKS:
            func_a = load_entry_function(std_path(std_dir, task_id), f'qiskit_a_code{task_id}', spec.entrypoint)
    except Exception:
        result['setup_error'] = traceback.format_exc().strip()
        return result
    qiskit_cases = build_qiskit_cases()
    framework_cases = build_pennylane_cases()
    all_passed = True
    for index, qiskit_case in enumerate(qiskit_cases[task_id], start=1):
        framework_case = framework_cases[task_id][index - 1]
        row = evaluate_case(task_id, func_a, func_b, qiskit_case, framework_case, index)
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

def aggregate_case_status(cases: list[dict[str, Any]]) -> str:
    statuses = [str(case.get('status', 'FAIL')) for case in cases]
    return 'PASS' if statuses and all((status == 'PASS' for status in statuses)) else 'FAIL'

def evaluate_case(task_id: int, func_a: Callable[..., Any] | None, func_b: Callable[..., Any], qiskit_case: dict[str, Any], framework_case: dict[str, Any], index: int) -> dict[str, Any]:
    if task_id in STATE_TASKS:
        if func_a is None:
            raise ValueError(f'task {task_id} requires a reference function')
        return evaluate_state_case(task_id, func_a, func_b, qiskit_case, framework_case, index)
    if task_id in CIRCUIT_STATE_TASKS:
        if func_a is None:
            raise ValueError(f'task {task_id} requires a reference function')
        return evaluate_circuit_state_case(task_id, func_a, func_b, qiskit_case, framework_case, index)
    if task_id == 83:
        return evaluate_bell_properties_case(func_b, framework_case, index)
    return evaluate_property_case(task_id, func_b, framework_case, index)

def evaluate_state_case(task_id: int, func_a: Callable[..., Any], func_b: Callable[..., Any], qiskit_case: dict[str, Any], framework_case: dict[str, Any], index: int) -> dict[str, Any]:
    label = qiskit_case.get('label', f'case_{index}')
    row = base_case_row(label)
    outcome_a = call_and_capture(func_a, clone_value(tuple(qiskit_case.get('args', ()))), clone_value(dict(qiskit_case.get('kwargs', {}))))
    outcome_b = call_pennylane_candidate(func_b, clone_value(tuple(framework_case.get('args', ()))), clone_value(dict(framework_case.get('kwargs', {}))))
    if outcome_a['error'] or outcome_b['error']:
        row['error'] = combine_errors(outcome_a, outcome_b)
        return row
    try:
        value_a = outcome_a['value']
        value_b = outcome_b['value']
        if task_id == 139:
            value_a = reconstruct_schmidt_state(value_a)
            value_b = reconstruct_pennylane_schmidt_output(value_b)
            metrics = compare_quantum_states(value_a, value_b)
        else:
            candidate_states = collect_pennylane_state_candidates(value_b)
            metrics = best_quantum_state_comparison(value_a, candidate_states)
    except Exception:
        row['error'] = f'METRIC ERROR:\n{traceback.format_exc().strip()}'
        return row
    row.update(metrics)
    row['status'] = 'PASS' if state_metrics_pass(metrics) else 'FAIL'
    return row

def evaluate_circuit_state_case(task_id: int, func_a: Callable[..., Any], func_b: Callable[..., Any], qiskit_case: dict[str, Any], framework_case: dict[str, Any], index: int) -> dict[str, Any]:
    from qiskit.quantum_info import Statevector
    label = qiskit_case.get('label', f'case_{index}')
    row = base_case_row(label)
    outcome_a = call_and_capture(func_a, clone_value(tuple(qiskit_case.get('args', ()))), clone_value(dict(qiskit_case.get('kwargs', {}))))
    outcome_b = call_pennylane_candidate(func_b, clone_value(tuple(framework_case.get('args', ()))), clone_value(dict(framework_case.get('kwargs', {}))))
    if outcome_a['error'] or outcome_b['error']:
        row['error'] = combine_errors(outcome_a, outcome_b)
        return row
    try:
        qiskit_circuit = coerce_reference_qiskit_circuit(outcome_a['value'])
        if task_id in CIRCUIT_STATE_TASKS:
            qiskit_circuit = qiskit_circuit.copy()
            qiskit_circuit.remove_final_measurements()
        value_a = Statevector.from_instruction(qiskit_circuit)
        candidate_states = collect_pennylane_state_candidates(outcome_b['value'])
        metrics = best_quantum_state_comparison(value_a, candidate_states)
    except Exception:
        row['error'] = f'METRIC ERROR:\n{traceback.format_exc().strip()}'
        return row
    row.update(metrics)
    row['status'] = 'PASS' if state_metrics_pass(metrics) else 'FAIL'
    return row

def evaluate_property_case(task_id: int, func_b: Callable[..., Any], framework_case: dict[str, Any], index: int) -> dict[str, Any]:
    label = framework_case.get('label', f'case_{index}')
    row = base_case_row(label)
    outcome = call_pennylane_candidate(func_b, clone_value(tuple(framework_case.get('args', ()))), clone_value(dict(framework_case.get('kwargs', {}))))
    if outcome['error']:
        row['error'] = format_outcome_error('B', outcome)
        return row
    try:
        normalized = normalize_pennylane_property_output(task_id, outcome['value'])
        metrics = evaluate_property_output(task_id, normalized)
    except Exception:
        row['error'] = f'METRIC ERROR:\n{traceback.format_exc().strip()}'
        return row
    passed = bool(metrics.pop('_passed'))
    row.update(metrics)
    row['status'] = 'PASS' if passed else 'FAIL'
    return row

def evaluate_bell_properties_case(func_b: Callable[..., Any], framework_case: dict[str, Any], index: int) -> dict[str, Any]:
    from qiskit.quantum_info import Statevector, concurrence
    label = framework_case.get('label', f'case_{index}')
    row = base_case_row(label)
    outcome = call_pennylane_candidate(func_b, clone_value(tuple(framework_case.get('args', ()))), clone_value(dict(framework_case.get('kwargs', {}))))
    if outcome['error']:
        row['error'] = format_outcome_error('B', outcome)
        return row
    try:
        density, returned_concurrence = normalize_pennylane_bell_output(outcome['value'])
        candidate_density = as_density_matrix(density)
        expected_density = as_density_matrix((Statevector.from_label('00') + Statevector.from_label('11')) / math.sqrt(2))
        metrics = compare_quantum_states(expected_density, candidate_density)
        dims = tuple((int(part) for part in candidate_density.dims()))
        returned = float(returned_concurrence)
        recalculated = float(concurrence(candidate_density))
        concurrence_ok = abs(returned - 1.0) <= 1e-06 and abs(recalculated - 1.0) <= 1e-06 and (abs(returned - recalculated) <= 1e-06)
    except Exception:
        row['error'] = f'METRIC ERROR:\n{traceback.format_exc().strip()}'
        return row
    row.update(metrics)
    row['metric_name'] = 'bell_density_and_concurrence'
    row['min_metric'] = min(returned, recalculated)
    row['max_metric'] = max(returned, recalculated)
    if dims != (2, 2):
        row['failed_items'].append({'index': 0, 'dims': dims})
    if not concurrence_ok:
        row['failed_items'].append({'index': 1, 'returned_concurrence': returned, 'recalculated_concurrence': recalculated})
    row['status'] = 'PASS' if state_metrics_pass(metrics) and dims == (2, 2) and concurrence_ok else 'FAIL'
    return row

def coerce_reference_qiskit_circuit(value: Any) -> Any:
    from qiskit import QuantumCircuit
    if isinstance(value, QuantumCircuit):
        return value
    if isinstance(value, (tuple, list)) and value and isinstance(value[0], QuantumCircuit):
        return value[0]
    raise TypeError(f'Expected QuantumCircuit output, got {type(value).__name__}')

def call_pennylane_candidate(func: Callable[..., Any], args: tuple[Any, ...], kwargs: dict[str, Any], timeout_seconds: float=CASE_TIMEOUT_SECONDS) -> dict[str, Any]:
    source_path = getattr(func, '__eval_source_path__', None)
    module_name = getattr(func, '__eval_module_name__', None)
    entrypoint = getattr(func, '__eval_entrypoint__', None)
    if not source_path or not module_name or (not entrypoint):
        return {'value': None, 'error': 'INTERNAL ERROR: function lacks eval metadata', 'captured_stdout': ''}
    result_file = tempfile.NamedTemporaryFile(prefix='cross_eval_pennylane_', suffix='.pkl', delete=False)
    result_path = result_file.name
    result_file.close()
    process = mp.Process(target=call_pennylane_worker, args=(result_path, source_path, module_name, entrypoint, args, kwargs))
    try:
        process.start()
        process.join(timeout_seconds)
        if process.is_alive():
            process.terminate()
            process.join(5)
            if process.is_alive():
                process.kill()
                process.join()
            return {'value': None, 'error': f'TIMEOUT after {timeout_seconds:g}s', 'error_type': 'timeout', 'captured_stdout': ''}
        if Path(result_path).stat().st_size > 0:
            with open(result_path, 'rb') as handle:
                return pickle.load(handle)
        if process.exitcode not in (0, None):
            return {'value': None, 'error': f'PROCESS EXITED with code {process.exitcode}', 'error_type': 'evaluator_process_error', 'captured_stdout': ''}
        return {'value': None, 'error': 'PROCESS EXITED without result', 'error_type': 'evaluator_process_error', 'captured_stdout': ''}
    except Exception as exc:
        return {'value': None, 'error': f'PennyLane evaluator process failed: {short_error(exc)}', 'error_type': 'evaluator_process_error', 'captured_stdout': ''}
    finally:
        try:
            Path(result_path).unlink()
        except FileNotFoundError:
            pass

def call_pennylane_worker(result_path: str, source_path: str, module_name: str, entrypoint: str, args: tuple[Any, ...], kwargs: dict[str, Any]) -> None:
    try:
        func = load_entry_function(Path(source_path), module_name, entrypoint)
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            value = execute_pennylane_entry_function(func, args, kwargs)
        result = {'value': value, 'error': None, 'captured_stdout': stdout.getvalue()[-4000:]}
    except Exception as exc:
        result = {'value': None, 'error': traceback.format_exc().strip(), 'error_type': 'evaluator_serialization_error' if isinstance(exc, PennyLaneEvaluatorSerializationError) else 'unclassified_candidate_or_environment_error', 'captured_stdout': ''}
    with open(result_path, 'wb') as handle:
        pickle.dump(result, handle)

def execute_pennylane_entry_function(func: Callable[..., Any], args: tuple[Any, ...], kwargs: dict[str, Any]) -> Any:
    value, artifact = capture_outer_pennylane_execution(func, args, kwargs)
    if is_pennylane_tape(value):
        artifact = serialize_pennylane_tape_checked(value)
        value = None
    elif isinstance(value, tuple) and value:
        first = value[0]
        if is_pennylane_tape(first):
            artifact = serialize_pennylane_tape_checked(first)
            value = (None, *value[1:])
        elif is_pennylane_quantum_callable(first):
            converted, returned_artifact = capture_returned_quantum_callable(first)
            artifact = returned_artifact or artifact
            value = (converted, *value[1:])
    elif isinstance(value, list) and value:
        first = value[0]
        if is_pennylane_tape(first):
            artifact = serialize_pennylane_tape_checked(first)
            value = [None, *value[1:]]
        elif is_pennylane_quantum_callable(first):
            converted, returned_artifact = capture_returned_quantum_callable(first)
            artifact = returned_artifact or artifact
            value = [converted, *value[1:]]
    elif is_pennylane_quantum_callable(value):
        value, returned_artifact = capture_returned_quantum_callable(value)
        artifact = returned_artifact or artifact
    if artifact is not None:
        return build_pennylane_bundle(value, artifact)
    return value

def capture_outer_pennylane_execution(func: Callable[..., Any], args: tuple[Any, ...], kwargs: dict[str, Any]) -> tuple[Any, dict[str, Any] | None]:
    import pennylane as qml
    with qml.queuing.AnnotatedQueue() as queue:
        value = func(*args, **kwargs)
    returned_value = value
    if isinstance(returned_value, (tuple, list)) and returned_value:
        returned_value = returned_value[0]
    if is_pennylane_tape(returned_value):
        return (value, None)
    try:
        artifact = serialize_pennylane_queue(queue)
    except Exception as exc:
        raise PennyLaneEvaluatorSerializationError(f'Failed to serialize PennyLane execution queue: {exc}') from exc
    return (value, artifact)

def capture_returned_quantum_callable(value: Any) -> tuple[Any, dict[str, Any] | None]:
    import pennylane as qml
    if isinstance(value, qml.QNode):
        qfunc = getattr(value, 'func', None) or getattr(value, '_qfunc', None)
        if not callable(qfunc):
            qfunc = value
        with qml.queuing.AnnotatedQueue() as queue:
            queued_value = qfunc()
        try:
            artifact = serialize_pennylane_queue(queue)
        except Exception as exc:
            raise PennyLaneEvaluatorSerializationError(f'Failed to serialize returned QNode queue: {exc}') from exc
        executed_value = value()
        artifact = merge_artifact_device_wires(artifact, getattr(value.device, 'wires', None))
        return (executed_value if is_pickle_safe(executed_value) else queued_value, artifact)
    if callable(value):
        with qml.queuing.AnnotatedQueue() as queue:
            queued_value = value()
        try:
            artifact = serialize_pennylane_queue(queue)
        except Exception as exc:
            raise PennyLaneEvaluatorSerializationError(f'Failed to serialize returned quantum callable queue: {exc}') from exc
        return (queued_value, artifact)
    raise TypeError(f'Expected QNode or callable quantum function, got {type(value).__name__}')

def build_pennylane_bundle(raw: Any, artifact: dict[str, Any]) -> dict[str, Any]:
    return {PENNYLANE_BUNDLE_KEY: True, 'raw': raw if is_pickle_safe(raw) else None, 'artifact': artifact}

def split_pennylane_bundle(value: Any) -> tuple[Any, dict[str, Any] | None]:
    if isinstance(value, dict) and value.get(PENNYLANE_BUNDLE_KEY):
        return (value.get('raw'), value.get('artifact'))
    return (value, None)

def is_pickle_safe(value: Any) -> bool:
    try:
        pickle.dumps(value)
    except Exception:
        return False
    return True

def is_pennylane_quantum_callable(value: Any) -> bool:
    try:
        import pennylane as qml
    except Exception:
        return False
    if isinstance(value, qml.QNode):
        return True
    return callable(value)

def is_pennylane_tape(value: Any) -> bool:
    module_name = getattr(getattr(value, '__class__', None), '__module__', '')
    return module_name.startswith('pennylane') and hasattr(value, 'operations') and hasattr(value, 'measurements')

def serialize_pennylane_queue(queue: Any) -> dict[str, Any] | None:
    from pennylane.measurements import MeasurementProcess
    from pennylane.operation import Operator
    operations: list[dict[str, Any]] = []
    measurements: list[dict[str, Any]] = []
    wire_labels: list[Any] = []
    for queued_item in list(queue):
        item = unwrap_pennylane_queue_item(queued_item)
        if isinstance(item, MeasurementProcess):
            measurement = serialize_pennylane_measurement(item)
            measurements.append(measurement)
            extend_wire_labels(wire_labels, measurement['wires'])
            continue
        if isinstance(item, Operator):
            operation = serialize_pennylane_operation(item)
            operations.append(operation)
            extend_wire_labels(wire_labels, operation['wires'])
            continue
        raise TypeError(f'Unsupported PennyLane queue entry {type(item).__module__}.{type(item).__name__}; refusing to silently omit queued program content')
    if not operations and (not measurements):
        return None
    return {PENNYLANE_ARTIFACT_KEY: True, 'operations': operations, 'measurements': measurements, 'wire_labels': wire_labels}

def serialize_pennylane_tape(tape: Any) -> dict[str, Any] | None:
    operations = [serialize_pennylane_operation(operation) for operation in getattr(tape, 'operations', ())]
    measurements = [serialize_pennylane_measurement(measurement) for measurement in getattr(tape, 'measurements', ())]
    wire_labels: list[Any] = []
    for operation in operations:
        extend_wire_labels(wire_labels, operation['wires'])
    for measurement in measurements:
        extend_wire_labels(wire_labels, measurement['wires'])
    if not operations and (not measurements):
        return None
    return {PENNYLANE_ARTIFACT_KEY: True, 'operations': operations, 'measurements': measurements, 'wire_labels': wire_labels}

def serialize_pennylane_operation(operation: Any) -> dict[str, Any]:
    parameters = list(getattr(operation, 'parameters', getattr(operation, 'data', ())))
    return {'class_name': operation.__class__.__name__, 'wires': normalize_wire_sequence(getattr(operation, 'wires', ())), 'parameters': parameters}

def serialize_pennylane_measurement(measurement: Any) -> dict[str, Any]:
    observable = getattr(measurement, 'obs', None)
    return {'class_name': measurement.__class__.__name__, 'wires': normalize_wire_sequence(getattr(measurement, 'wires', ())), 'observable': None if observable is None else observable.__class__.__name__}

def normalize_wire_sequence(wires: Any) -> list[Any]:
    labels: list[Any] = []
    for wire in list(wires):
        if isinstance(wire, np.generic):
            wire = wire.item()
        labels.append(wire)
    return labels

def extend_wire_labels(target: list[Any], source: list[Any]) -> None:
    for wire in source:
        if wire not in target:
            target.append(wire)

def merge_artifact_device_wires(artifact: dict[str, Any] | None, wires: Any) -> dict[str, Any] | None:
    if artifact is None:
        return artifact
    for wire in normalize_wire_sequence(wires or ()):
        if wire not in artifact['wire_labels']:
            artifact['wire_labels'].append(wire)
    return artifact

def collect_pennylane_state_candidates(value: Any) -> list[Any]:
    raw, artifact = split_pennylane_bundle(value)
    candidates: list[Any] = []
    if artifact is not None:
        try:
            candidates.extend(density_matrix_order_variants(artifact_to_statevector(artifact)))
        except Exception:
            pass
    if raw is not None and (not candidates):
        try:
            candidates.extend(density_matrix_order_variants(raw))
        except Exception:
            pass
    if not candidates:
        raise TypeError('PennyLane candidate did not produce a state-like value, QNode, quantum function, or queued circuit')
    return deduplicate_density_candidates(candidates)

def deduplicate_density_candidates(candidates: list[Any]) -> list[Any]:
    unique: list[Any] = []
    seen: set[bytes] = set()
    for candidate in candidates:
        data = as_density_matrix(candidate).data
        key = np.asarray(data, dtype=complex).tobytes()
        if key in seen:
            continue
        seen.add(key)
        unique.append(candidate)
    return unique

def density_matrix_order_variants(value: Any) -> list[Any]:
    density = as_density_matrix(value)
    variants = [density]
    reversed_density = reverse_qubit_order_density_matrix(density)
    if reversed_density is not None:
        original = np.asarray(density.data, dtype=complex)
        reversed_data = np.asarray(reversed_density.data, dtype=complex)
        if reversed_data.tobytes() != original.tobytes():
            variants.append(reversed_density)
    return variants

def reverse_qubit_order_density_matrix(value: Any) -> Any | None:
    from qiskit.quantum_info import DensityMatrix
    density = as_density_matrix(value).data
    array = np.asarray(density, dtype=complex)
    if array.ndim != 2 or array.shape[0] != array.shape[1]:
        return None
    dim = int(array.shape[0])
    if dim == 0 or dim & dim - 1:
        return None
    num_qubits = int(math.log2(dim))
    if 2 ** num_qubits != dim or num_qubits <= 1:
        return None
    permutation = [reverse_bits(index, num_qubits) for index in range(dim)]
    return DensityMatrix(array[np.ix_(permutation, permutation)])

def artifact_to_statevector(artifact: dict[str, Any]) -> Any:
    import pennylane as qml
    wire_labels = artifact.get('wire_labels') or infer_wire_labels_from_artifact(artifact)
    if not wire_labels:
        raise ValueError('Unable to infer PennyLane wires from candidate artifact')
    dev = qml.device('default.qubit', wires=wire_labels)

    @qml.qnode(dev)
    def state_circuit():
        replay_pennylane_artifact(artifact)
        return qml.state()
    return np.asarray(state_circuit(), dtype=complex).reshape(-1)

def artifact_to_density_matrix(artifact: dict[str, Any], wires: list[Any] | None=None) -> Any:
    import pennylane as qml
    wire_labels = artifact.get('wire_labels') or infer_wire_labels_from_artifact(artifact)
    if not wire_labels:
        raise ValueError('Unable to infer PennyLane wires from candidate artifact')
    target_wires = wires or wire_labels
    dev = qml.device('default.qubit', wires=wire_labels)

    @qml.qnode(dev)
    def density_circuit():
        replay_pennylane_artifact(artifact)
        return qml.density_matrix(wires=target_wires)
    return np.asarray(density_circuit(), dtype=complex)

def replay_pennylane_artifact(artifact: dict[str, Any]) -> None:
    import pennylane as qml
    for operation in artifact.get('operations', ()):
        op_cls = getattr(qml, operation['class_name'], None)
        if op_cls is None:
            op_cls = getattr(getattr(qml, 'ops', None), operation['class_name'], None)
        if op_cls is None:
            raise ValueError(f'Unsupported PennyLane operation in evaluator: {operation['class_name']}')
        op_cls(*operation.get('parameters', ()), wires=operation.get('wires', ()))

def infer_wire_labels_from_artifact(artifact: dict[str, Any]) -> list[Any]:
    wire_labels: list[Any] = []
    for operation in artifact.get('operations', ()):
        extend_wire_labels(wire_labels, list(operation.get('wires', ())))
    for measurement in artifact.get('measurements', ()):
        extend_wire_labels(wire_labels, list(measurement.get('wires', ())))
    return wire_labels

def reconstruct_pennylane_schmidt_output(value: Any) -> Any:
    raw, artifact = split_pennylane_bundle(value)
    if artifact is not None and raw is None:
        raise TypeError('Expected Schmidt decomposition terms, got only a queued PennyLane circuit')
    return reconstruct_schmidt_state(raw)

def normalize_pennylane_property_output(task_id: int, value: Any) -> Any:
    quantum_mode = 'state' if task_id == 143 else 'density'
    raw, artifact = split_pennylane_bundle(value)
    if raw is not None:
        return normalize_nested_pennylane_value(raw, quantum_mode)
    if artifact is None:
        raise TypeError('Expected a dataset-like output from PennyLane candidate')
    return artifact_to_quantum_value(artifact, quantum_mode)

def normalize_pennylane_bell_output(value: Any) -> tuple[Any, Any]:
    raw, artifact = split_pennylane_bundle(value)
    if raw is None:
        raise TypeError('Expected a pair of (density, concurrence), got only a queued PennyLane circuit')
    density, concurrence_value = coerce_pair(raw)
    try:
        as_density_matrix(density)
    except Exception:
        if artifact is None:
            raise
        density = artifact_to_density_matrix(artifact)
    return (density, concurrence_value)

def normalize_nested_pennylane_value(value: Any, quantum_mode: str) -> Any:
    raw, artifact = split_pennylane_bundle(value)
    if artifact is not None:
        if raw is not None:
            return normalize_nested_pennylane_value(raw, quantum_mode)
        return artifact_to_quantum_value(artifact, quantum_mode)
    if isinstance(value, list):
        return [normalize_nested_pennylane_value(item, quantum_mode) for item in value]
    if isinstance(value, tuple):
        return tuple((normalize_nested_pennylane_value(item, quantum_mode) for item in value))
    return value

def artifact_to_quantum_value(artifact: dict[str, Any], quantum_mode: str) -> Any:
    if quantum_mode == 'state':
        return artifact_to_statevector(artifact)
    if quantum_mode == 'density':
        return artifact_to_density_matrix(artifact)
    raise ValueError(f'Unsupported quantum_mode: {quantum_mode}')

def build_environment_info() -> dict[str, Any]:
    packages = {}
    for package in ('pennylane', 'numpy', 'qiskit', 'qiskit-aer', 'qiskit-ibm-runtime'):
        try:
            packages[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            packages[package] = None
    return {'python': platform.python_version(), 'platform': platform.platform(), 'packages': packages}

def build_raw_details(sample_results: list[dict[str, Any]], std_dir: Path, candidate_dir: Path, model: str, framework: str) -> dict[str, Any]:
    grouped: dict[int, list[dict[str, Any]]] = {}
    for sample in sample_results:
        grouped.setdefault(int(sample['task_id']), []).append(sample)
    results: list[dict[str, Any]] = []
    for task_id in sorted(grouped):
        samples = sorted(grouped[task_id], key=lambda sample: int(sample.get('sample_index') or 0))
        first = samples[0]
        pass_count, pass_at_1, pass_at_3, pass_at_5 = task_pass_metrics(samples)
        best_sample = next((sample for sample in samples if sample.get('raw_label') == 'PASS'), None)
        results.append({'task_id': task_id, 'class_id': first.get('class_id'), 'path_a': first.get('path_a'), 'path_b': first.get('path_b'), 'framework': framework, 'function': first.get('function'), 'samples': samples, 'sample_count': len(samples), 'pass_count': pass_count, 'pass_at_1': pass_at_1, 'pass_at_3': pass_at_3, 'pass_at_5': pass_at_5, 'best_sample_index': None if best_sample is None else best_sample.get('sample_index'), 'best_sample_path': None if best_sample is None else best_sample.get('candidate_path'), 'raw_status': aggregate_task_status(samples), 'raw_label': 'PASS' if pass_count > 0 else 'FAIL', 'setup_error': None if samples else 'No samples'})
    return {'mode': 'cross_language', 'class_id': 2, 'model': model, 'framework': framework, 'dir_a': str(std_dir), 'dir_b': str(candidate_dir), 'thresholds': thresholds(), 'environment': build_environment_info(), 'summary': {}, 'results': results}

def serialize_pennylane_tape_checked(tape: Any) -> dict[str, Any] | None:
    try:
        return serialize_pennylane_tape(tape)
    except Exception as exc:
        raise PennyLaneEvaluatorSerializationError(f'Failed to serialize PennyLane QuantumScript: {exc}') from exc

def unwrap_pennylane_queue_item(item: Any) -> Any:
    while item.__class__.__name__ == 'WrappedObj' and getattr(item.__class__, '__module__', '').startswith('pennylane'):
        if not hasattr(item, 'obj'):
            raise TypeError('PennyLane WrappedObj queue entry has no obj payload')
        unwrapped = item.obj
        if unwrapped is item:
            raise TypeError('PennyLane WrappedObj queue entry refers to itself')
        item = unwrapped
    return item
