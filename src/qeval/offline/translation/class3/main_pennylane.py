import importlib.metadata
import inspect
import platform
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import main as base
from tasks import get_task_spec
FRAMEWORKS = ('pennylane',)
FRAMEWORK_NAMES = {**base.FRAMEWORK_NAMES, 'pennylane': 'PennyLane'}
FRAMEWORK_PACKAGES = {**base.FRAMEWORK_PACKAGES, 'pennylane': 'pennylane==0.45.1'}
ORIGINAL_BUILD_TRANSLATION_PROMPT = base.build_translation_prompt
ORIGINAL_CONVERT_VALUE_FOR_FRAMEWORK = base.convert_value_for_framework
ORIGINAL_TO_OPERATOR = base.to_operator
ORIGINAL_TO_OPERATOR_VARIANTS = base.to_operator_variants
ORIGINAL_TO_CHANNEL_VARIANTS = base.to_channel_variants
ORIGINAL_BIND_PARAMETERS = base.bind_parameters
ORIGINAL_CALL_AND_CAPTURE = base.call_and_capture

@dataclass(frozen=True)
class PennylaneSymbol:
    name: str

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

def parse_frameworks(raw: str) -> list[str]:
    frameworks = [item.strip().lower() for item in raw.split(',') if item.strip()]
    if not frameworks:
        raise ValueError('At least one framework is required.')
    unknown = sorted(set(frameworks).difference(FRAMEWORKS))
    if unknown:
        raise ValueError(f'Unsupported framework(s): {unknown}')
    return frameworks

def build_translation_prompt(task_id: int, framework: str, std_dir: Path) -> str:
    if framework == 'pennylane':
        return build_pennylane_prompt(task_id, std_dir)
    return ORIGINAL_BUILD_TRANSLATION_PROMPT(task_id, framework, std_dir)

def build_pennylane_prompt(task_id: int, std_dir: Path) -> str:
    spec = get_task_spec(task_id)
    qiskit_code = base.strip_existing_eval_meta(base.read_text_auto(base.std_path(std_dir, task_id))).strip()
    return f'Translate the verified Qiskit reference solution below into pennylane Python code.\n\nThis is a code translation task, not a from-scratch benchmark solve. Use the Qiskit code as the semantic source of truth.\n\nTarget pennylane environment:\n- pennylane==0.45.1\n\nOutput rules:\n- Output only the EVAL_META line, imports, and the required function.\n- Do not explain. Do not reason. Output code only.\n- Do not import qiskit.\n- Do not hard-code fixed benchmark answers.\n- The first line must be exactly:\n# EVAL_META: task_id={task_id}, framework=pennylane, class=3\n- Keep the same entry function name and the same number of arguments: {spec.entrypoint}.\n\nOriginal Qiskit task:\nTask:\n- Task id: {task_id}\n- Description: {spec.description}\n- Function signature: {spec.signature}\n- Required return format: {spec.return_format}\n\nVerified Qiskit reference solution:\n# EVAL_META: task_id={task_id}, framework=qiskit, class=3\n{qiskit_code}\n'

def convert_value_for_framework(value: Any, framework: str, task_id: int) -> Any:
    if framework == 'pennylane':
        return convert_value_to_pennylane(value, task_id)
    return ORIGINAL_CONVERT_VALUE_FOR_FRAMEWORK(value, framework, task_id)

def convert_value_to_pennylane(value: Any, task_id: int) -> Any:
    if base.is_qiskit_quantum_circuit(value):
        return qiskit_circuit_to_pennylane(value, task_id)
    if base.is_qiskit_operator_like(value):
        return base.qiskit_operator_matrix(value)
    if isinstance(value, list):
        return [convert_value_to_pennylane(item, task_id) for item in value]
    if isinstance(value, tuple):
        return tuple((convert_value_to_pennylane(item, task_id) for item in value))
    return base.clone_value(value)

def qiskit_circuit_to_pennylane(circuit: Any, task_id: int) -> Any:
    import pennylane as qml
    operations: list[Any] = []
    measurements: list[Any] = []
    for instruction in circuit.data:
        operation = instruction.operation
        qargs = [circuit.find_bit(qubit).index for qubit in instruction.qubits]
        name = operation.name.lower()
        if name == 'measure':
            if qargs:
                measurements.append(qml.sample(wires=qargs[0]))
            continue
        gate = pennylane_gate_for_qiskit_operation(operation, qargs)
        if gate is not None:
            operations.append(gate)
    if task_id == 147 and (not operations):
        script = make_quantum_script([], [], circuit.num_qubits, circuit.num_clbits)
        return script
    return make_quantum_script(operations, measurements, circuit.num_qubits, circuit.num_clbits)

def pennylane_gate_for_qiskit_operation(operation: Any, qargs: list[int]) -> Any | None:
    import pennylane as qml
    name = operation.name.lower()
    params = list(getattr(operation, 'params', []) or [])
    if name == 'barrier':
        return None
    if name in {'id', 'i'}:
        return qml.Identity(wires=qargs[0])
    if name == 'h':
        return qml.Hadamard(wires=qargs[0])
    if name == 'x':
        return qml.PauliX(wires=qargs[0])
    if name == 'y':
        return qml.PauliY(wires=qargs[0])
    if name == 'z':
        return qml.PauliZ(wires=qargs[0])
    if name == 's':
        return qml.S(wires=qargs[0])
    if name == 'sdg':
        return qml.adjoint(qml.S(wires=qargs[0]))
    if name == 't':
        return qml.T(wires=qargs[0])
    if name == 'tdg':
        return qml.adjoint(qml.T(wires=qargs[0]))
    if name == 'sx':
        return qml.SX(wires=qargs[0])
    if name == 'sxdg':
        return qml.adjoint(qml.SX(wires=qargs[0]))
    if name in {'cx', 'cnot'}:
        return qml.CNOT(wires=qargs)
    if name == 'cz':
        return qml.CZ(wires=qargs)
    if name == 'swap':
        return qml.SWAP(wires=qargs)
    if name == 'ccx':
        return qml.Toffoli(wires=qargs)
    if name == 'rx':
        return qml.RX(pennylane_param(params[0]), wires=qargs[0])
    if name == 'ry':
        return qml.RY(pennylane_param(params[0]), wires=qargs[0])
    if name == 'rz':
        return qml.RZ(pennylane_param(params[0]), wires=qargs[0])
    if name in {'p', 'u1'}:
        return qml.PhaseShift(pennylane_param(params[0]), wires=qargs[0])
    if name == 'u2':
        return qml.U2(*(pennylane_param(param) for param in params), wires=qargs[0])
    if name == 'u':
        return qml.U3(*(pennylane_param(param) for param in params), wires=qargs[0])
    if hasattr(operation, 'to_matrix'):
        return qml.QubitUnitary(operation.to_matrix(), wires=qargs)
    raise TypeError(f'Unsupported Qiskit operation for PennyLane conversion: {name}')

def pennylane_param(value: Any) -> Any:
    try:
        return float(value)
    except (TypeError, ValueError):
        return PennylaneSymbol(getattr(value, 'name', str(value)))

def compare_outputs(reference: Any, candidate: Any) -> dict[str, Any]:
    if isinstance(candidate, (list, tuple)) and len(candidate) == 0 and base.is_qiskit_quantum_circuit(reference):
        candidate = make_quantum_script([], [], reference.num_qubits, reference.num_clbits)
    is_sequence = is_output_sequence(reference) or is_output_sequence(candidate)
    reference_items = normalize_output(reference)
    candidate_items = normalize_output(candidate)
    if len(reference_items) != len(candidate_items):
        raise ValueError(f'list length mismatch: reference={len(reference_items)}, candidate={len(candidate_items)}')
    item_metrics = [base.compare_one(ref_item, cand_item) for ref_item, cand_item in zip(reference_items, candidate_items)]
    return base.aggregate_item_metrics(item_metrics, is_sequence=is_sequence)

def compare_candidate_sequence_to_reference(candidate: Any, reference: Any) -> dict[str, Any]:
    candidate_items = normalize_sequence_output(candidate)
    if not candidate_items:
        raise ValueError('list length mismatch: reference>=1, candidate=0')
    item_metrics = [base.compare_one(reference, candidate_item) for candidate_item in candidate_items]
    return base.aggregate_item_metrics(item_metrics, is_sequence=True)

def normalize_output(value: Any) -> list[Any]:
    if is_pennylane_operation_sequence(value):
        return [pennylane_sequence_to_quantum_script(value)]
    if isinstance(value, (list, tuple)):
        return list(value)
    return [value]

def normalize_sequence_output(value: Any) -> list[Any]:
    if is_pennylane_operation_sequence(value):
        return [pennylane_sequence_to_quantum_script(value)]
    if not isinstance(value, (list, tuple)):
        raise TypeError(f'Expected list or tuple output, got {type(value).__name__}')
    return list(value)

def is_output_sequence(value: Any) -> bool:
    return isinstance(value, (list, tuple)) and (not is_pennylane_operation_sequence(value))

def is_pennylane_operation_sequence(value: Any) -> bool:
    if not isinstance(value, (list, tuple)) or not value:
        return False
    return all((is_pennylane_operation(item) or is_pennylane_measurement(item) for item in value))

def pennylane_sequence_to_quantum_script(value: list[Any] | tuple[Any, ...]) -> Any:
    operations = [item for item in value if is_pennylane_operation(item)]
    measurements = [item for item in value if is_pennylane_measurement(item)]
    wire_order = infer_wires_from_items([*operations, *measurements])
    return make_quantum_script(operations, measurements, len(wire_order), 0, declared_wires=wire_order)

def to_operator_variants(value: Any, *, expected_num_qubits: int | None=None) -> list[Any]:
    from qiskit.quantum_info import Operator
    prepared = bind_parameters(value)
    if is_pennylane_compatible(prepared):
        return [Operator(matrix) for matrix in pennylane_matrix_variants(prepared)]
    return ORIGINAL_TO_OPERATOR_VARIANTS(prepared)

def to_channel_variants(value: Any, reference_channel: Any) -> list[Any]:
    from qiskit.quantum_info import Choi, Operator
    prepared = bind_parameters(value)
    if is_pennylane_compatible(prepared):
        variants = []
        for matrix in pennylane_matrix_variants(prepared):
            if matrix.shape == getattr(reference_channel, 'data', ()).shape:
                variants.append(Choi(matrix))
            else:
                variants.append(Operator(matrix))
        return variants
    return ORIGINAL_TO_CHANNEL_VARIANTS(prepared, reference_channel)

def to_operator(value: Any) -> Any:
    from qiskit.quantum_info import Operator
    prepared = bind_parameters(value)
    if is_pennylane_compatible(prepared):
        return Operator(pennylane_matrix_variants(prepared)[0])
    return ORIGINAL_TO_OPERATOR(prepared)

def bind_parameters(value: Any) -> Any:
    if is_pennylane_qnode(value):
        return bind_pennylane_quantum_script(pennylane_qnode_to_quantum_script(value))
    if is_pennylane_callable(value):
        return bind_pennylane_quantum_script(pennylane_callable_to_quantum_script(value))
    if is_pennylane_operation_sequence(value):
        return bind_pennylane_quantum_script(pennylane_sequence_to_quantum_script(value))
    if is_pennylane_quantum_script(value):
        return bind_pennylane_quantum_script(value)
    if is_pennylane_operation(value):
        return bind_pennylane_operation(value)
    parameters = list(getattr(value, 'parameters', []) or [])
    if parameters and hasattr(value, 'assign_parameters'):
        ordered_parameters = sorted(parameters, key=qiskit_parameter_sort_key)
        assignments = {parameter: base.PARAMETER_VALUES[index % len(base.PARAMETER_VALUES)] for index, parameter in enumerate(ordered_parameters)}
        return value.assign_parameters(assignments)
    return ORIGINAL_BIND_PARAMETERS(value)

def qiskit_parameter_sort_key(parameter: Any) -> tuple[str, int, int, str]:
    vector = getattr(parameter, 'vector', None)
    index = getattr(parameter, 'index', None)
    name = str(getattr(parameter, 'name', parameter))
    if vector is not None and isinstance(index, int):
        return (str(getattr(vector, 'name', vector)), 0, index, name)
    return (name, 1, 0, name)

def bind_pennylane_quantum_script(script: Any) -> Any:
    parameters = list(script.get_parameters(trainable_only=False))
    assignments = build_symbol_assignments(parameters)
    new_params: list[Any] = []
    indices: list[int] = []
    for index, parameter in enumerate(parameters):
        if not is_numeric_parameter(parameter):
            new_params.append(bind_symbolic_parameter(parameter, assignments))
            indices.append(index)
    if not indices:
        return script
    bound = script.bind_new_parameters(new_params, indices)
    copy_pennylane_metadata(script, bound)
    return bound

def bind_pennylane_operation(operation: Any) -> Any:
    import pennylane.ops.functions as op_functions
    parameters = list(getattr(operation, 'data', ()))
    assignments = build_symbol_assignments(parameters)
    new_params: list[Any] = []
    changed = False
    for parameter in parameters:
        if is_numeric_parameter(parameter):
            new_params.append(parameter)
        else:
            new_params.append(bind_symbolic_parameter(parameter, assignments))
            changed = True
    if not changed:
        return operation
    return op_functions.bind_new_parameters(operation, new_params)

def build_symbol_assignments(parameters: list[Any]) -> dict[str, Any]:
    names: set[str] = set()
    for parameter in parameters:
        if is_numeric_parameter(parameter):
            continue
        if isinstance(parameter, PennylaneSymbol):
            names.add(parameter.name)
            continue
        free_symbols = getattr(parameter, 'free_symbols', None)
        if free_symbols is not None:
            names.update((symbol_name(symbol) for symbol in free_symbols))
        else:
            names.add(symbol_name(parameter))
    ordered_names = sorted(names, key=symbol_sort_key)
    return {name: base.PARAMETER_VALUES[index % len(base.PARAMETER_VALUES)] for index, name in enumerate(ordered_names)}

def symbol_sort_key(name: str) -> tuple[str, int, int, str]:
    match = re.fullmatch('(.*?)(?:\\[(\\d+)\\]|_(\\d+))', name)
    if match:
        index = int(match.group(2) or match.group(3))
        return (match.group(1), 0, index, name)
    return (name, 1, 0, name)

def bind_symbolic_parameter(parameter: Any, assignments: dict[str, Any]) -> Any:
    if isinstance(parameter, PennylaneSymbol):
        return assignments[parameter.name]
    free_symbols = getattr(parameter, 'free_symbols', None)
    if free_symbols:
        substitutions = {symbol: assignments[symbol_name(symbol)] for symbol in free_symbols}
        bound = parameter.subs(substitutions)
        try:
            return float(bound)
        except (TypeError, ValueError) as exc:
            raise TypeError(f'PennyLane symbolic parameter did not resolve to a real scalar: {parameter!r}') from exc
    return assignments[symbol_name(parameter)]

def symbol_name(value: Any) -> str:
    return getattr(value, 'name', str(value))

def is_numeric_parameter(value: Any) -> bool:
    if isinstance(value, PennylaneSymbol):
        return False
    if isinstance(value, (str, bytes)):
        return False
    try:
        import numpy as np
        array = np.asarray(value)
    except Exception:
        return False
    return bool(array.size) and getattr(array.dtype, 'kind', '') in {'b', 'i', 'u', 'f', 'c'}

def is_pennylane_compatible(value: Any) -> bool:
    return is_pennylane_quantum_script(value) or is_pennylane_operation(value) or is_pennylane_operation_sequence(value) or is_pennylane_qnode(value) or is_pennylane_callable(value)

def is_pennylane_quantum_script(value: Any) -> bool:
    try:
        import pennylane as qml
    except Exception:
        return False
    return isinstance(value, qml.tape.QuantumScript)

def is_pennylane_operation(value: Any) -> bool:
    try:
        import pennylane as qml
    except Exception:
        return False
    return isinstance(value, qml.operation.Operator)

def is_pennylane_qnode(value: Any) -> bool:
    try:
        import pennylane as qml
    except Exception:
        return False
    return isinstance(value, qml.QNode)

def is_pennylane_callable(value: Any) -> bool:
    if not callable(value):
        return False
    if isinstance(value, type):
        return False
    if isinstance(value, (str, bytes)):
        return False
    if is_pennylane_qnode(value):
        return False
    if is_pennylane_quantum_script(value) or is_pennylane_operation(value) or is_pennylane_measurement(value):
        return False
    qml_module = getattr(value, '__globals__', {}).get('qml')
    return getattr(qml_module, '__name__', '') == 'pennylane'

def pennylane_qnode_to_quantum_script(value: Any) -> Any:
    args, kwargs = build_pennylane_call_args(value.func)
    script = value.construct(args=args, kwargs=kwargs)
    apply_pennylane_callable_metadata(script, value)
    return script

def pennylane_callable_to_quantum_script(value: Any, args: tuple[Any, ...] | None=None, kwargs: dict[str, Any] | None=None) -> Any:
    import pennylane as qml
    if args is None or kwargs is None:
        args, kwargs = build_pennylane_call_args(value)
    script = qml.tape.make_qscript(value)(*args, **kwargs)
    apply_pennylane_callable_metadata(script, value)
    return script

def build_pennylane_call_args(value: Any) -> tuple[tuple[Any, ...], dict[str, Any]]:
    args: list[Any] = []
    kwargs: dict[str, Any] = {}
    next_value = 0
    signature = inspect.signature(value)
    for parameter in signature.parameters.values():
        if parameter.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            continue
        if parameter.default is not inspect._empty and parameter.default is not None:
            continue
        assigned = base.PARAMETER_VALUES[next_value % len(base.PARAMETER_VALUES)]
        next_value += 1
        if parameter.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD):
            args.append(assigned)
        else:
            kwargs[parameter.name] = assigned
    return (tuple(args), kwargs)

def apply_pennylane_callable_metadata(script: Any, source: Any) -> None:
    import pennylane as qml
    declared_wires = list(getattr(script, 'wires', []) or [])
    device = getattr(source, 'device', None)
    if device is not None:
        declared_wires = list(getattr(device, 'wires', []) or declared_wires)
        if not declared_wires:
            num_wires = getattr(device, 'num_wires', None)
            if num_wires:
                declared_wires = list(range(int(num_wires)))
    declared_wires = normalize_pennylane_wires(declared_wires)
    if declared_wires:
        script.declared_wires = qml.wires.Wires(declared_wires)
        script.num_qubits = len(declared_wires)
    elif not hasattr(script, 'num_qubits'):
        script.num_qubits = 0
    if not hasattr(script, 'num_clbits'):
        script.num_clbits = 0
    if not hasattr(script, 'classical_bits'):
        script.classical_bits = []

def normalize_pennylane_wires(wires: list[Any]) -> list[Any]:
    if not wires:
        return []
    if all((isinstance(wire, int) and wire >= 0 for wire in wires)):
        return list(range(max(wires) + 1))
    return wires

def call_and_capture(func: Any, args: tuple[Any, ...], kwargs: dict[str, Any]) -> dict[str, Any]:
    outcome = ORIGINAL_CALL_AND_CAPTURE(func, args, kwargs)
    if outcome['error'] or outcome['value'] is not None:
        return outcome
    if not is_pennylane_callable(func):
        return outcome
    try:
        script = pennylane_callable_to_quantum_script(func, args, kwargs)
    except Exception:
        return outcome
    if not getattr(script, 'operations', None) and (not getattr(script, 'measurements', None)):
        return outcome
    return {'value': script, 'args': args, 'kwargs': kwargs, 'error': None}

def is_pennylane_measurement(value: Any) -> bool:
    try:
        import pennylane as qml
    except Exception:
        return False
    return isinstance(value, qml.measurements.MeasurementProcess)

def pennylane_matrix_variants(value: Any) -> list[Any]:
    import numpy as np
    import pennylane as qml
    prepared = bind_parameters(value)
    if is_pennylane_operation_sequence(prepared):
        prepared = pennylane_sequence_to_quantum_script(prepared)
    if is_pennylane_measurement(prepared):
        observable = getattr(prepared, 'obs', None)
        if observable is None:
            raise TypeError(f'Cannot convert {type(prepared).__name__} to a matrix')
        prepared = observable
    if is_pennylane_quantum_script(prepared):
        prepared = strip_pennylane_measurements(prepared)
    orders = pennylane_wire_orders(prepared)
    variants: list[Any] = []
    seen: set[bytes] = set()
    for order in orders:
        matrix = np.asarray(qml.matrix(prepared, wire_order=order), dtype=complex)
        marker = matrix.tobytes()
        if marker not in seen:
            seen.add(marker)
            variants.append(matrix)
    return variants

def strip_pennylane_measurements(script: Any) -> Any:
    if not getattr(script, 'measurements', None):
        return script
    stripped = make_quantum_script(list(script.operations), [], int(getattr(script, 'num_qubits', 0) or len(getattr(script, 'declared_wires', []) or [])), int(getattr(script, 'num_clbits', 0) or 0), declared_wires=list(getattr(script, 'declared_wires', []) or list(script.wires)))
    copy_pennylane_metadata(script, stripped)
    return stripped

def make_quantum_script(operations: list[Any], measurements: list[Any], num_qubits: int, num_clbits: int, *, declared_wires: list[Any] | None=None) -> Any:
    import pennylane as qml
    script = qml.tape.QuantumScript(list(operations), list(measurements))
    wire_order = list(declared_wires) if declared_wires is not None else list(range(num_qubits))
    script.declared_wires = qml.wires.Wires(wire_order)
    script.num_qubits = num_qubits
    script.num_clbits = num_clbits
    script.classical_bits = list(range(num_clbits))
    return script

def copy_pennylane_metadata(source: Any, target: Any) -> None:
    for attr in ('declared_wires', 'num_qubits', 'num_clbits', 'classical_bits'):
        if hasattr(source, attr):
            setattr(target, attr, getattr(source, attr))

def infer_wires_from_items(items: list[Any]) -> list[Any]:
    wires: list[Any] = []
    for item in items:
        for wire in list(getattr(item, 'wires', ())):
            if wire not in wires:
                wires.append(wire)
    return wires

def pennylane_wire_orders(value: Any) -> list[list[Any]]:
    declared = list(getattr(value, 'declared_wires', []) or [])
    wires = list(getattr(value, 'wires', []) or [])
    if not declared and (not wires):
        width = int(getattr(value, 'num_qubits', 0) or getattr(value, 'num_wires', 0) or 0)
        declared = list(range(width))
    base_order = declared or wires
    if not base_order:
        return [[]]
    reversed_order = list(reversed(base_order))
    if reversed_order == base_order:
        return [base_order]
    return [base_order, reversed_order]

def build_environment_info() -> dict[str, Any]:
    info: dict[str, Any] = {'python': platform.python_version(), 'platform': platform.platform(), 'packages': {}}
    for package in ('qiskit', 'qiskit-aer', 'qiskit-ibm-runtime', 'cirq', 'pyqpanda3', 'pennylane', 'numpy'):
        try:
            version = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            version = None
        info['packages'][package] = version
    return info

def patch_base() -> None:
    base.FRAMEWORKS = FRAMEWORKS
    base.FRAMEWORK_NAMES = FRAMEWORK_NAMES
    base.FRAMEWORK_PACKAGES = FRAMEWORK_PACKAGES
    base.parse_frameworks = parse_frameworks
    base.build_translation_prompt = build_translation_prompt
    base.convert_value_for_framework = convert_value_for_framework
    base.bind_parameters = bind_parameters
    base.to_operator = to_operator
    base.to_operator_variants = to_operator_variants
    base.to_channel_variants = to_channel_variants
    base.compare_outputs = compare_outputs
    base.compare_candidate_sequence_to_reference = compare_candidate_sequence_to_reference
    base.normalize_output = normalize_output
    base.normalize_sequence_output = normalize_sequence_output
    base.build_environment_info = build_environment_info
    base.is_pennylane_value = is_pennylane_compatible
    base.call_and_capture = call_and_capture
