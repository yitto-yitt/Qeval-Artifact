# EVAL_META: task_id=9, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit

try:
    from pyqpanda3.core import ParameterVector as _ParameterVector
    _HAS_PARAMETER_VECTOR = True
except ImportError:
    _HAS_PARAMETER_VECTOR = False

try:
    from pyqpanda3.core import Parameter as _Parameter
except ImportError:
    _Parameter = None


def create_efficientSU2():
    num_qubits = 3
    reps = 1
    num_rotation_layers = reps + 1
    gates_per_qubit = 2  # ry and rz
    num_params = num_rotation_layers * num_qubits * gates_per_qubit

    if _HAS_PARAMETER_VECTOR:
        params = _ParameterVector("θ", num_params)
    elif _Parameter is not None:
        params = [_Parameter(f"θ[{i}]") for i in range(num_params)]
    else:
        params = [0.0] * num_params

    circuit = QuantumCircuit(num_qubits)
    param_idx = 0

    def add_rotation_layer():
        nonlocal param_idx
        for q in range(num_qubits):
            circuit.ry(params[param_idx], q)
            param_idx += 1
            circuit.rz(params[param_idx], q)
            param_idx += 1

    for _ in range(reps):
        add_rotation_layer()
        circuit.barrier()

        # full entanglement
        for control in range(num_qubits):
            for target in range(control + 1, num_qubits):
                circuit.cx(control, target)
        circuit.barrier()

    add_rotation_layer()
    circuit.barrier()

    return circuit
