# EVAL_META: task_id=90, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def create_custom_controlled():
    x = np.array([[0, 1], [1, 0]], dtype=complex)
    h = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    custom = np.kron(x, h)

    with qml.tape.QuantumTape() as circuit:
        qml.ControlledQubitUnitary(custom, control_wires=[0, 3], wires=[1, 2])

    return circuit
