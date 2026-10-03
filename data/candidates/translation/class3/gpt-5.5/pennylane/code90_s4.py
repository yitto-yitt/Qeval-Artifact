# EVAL_META: task_id=90, framework=pennylane, class=3
import numpy as np
import pennylane as qml

def create_custom_controlled():
    x = np.array([[0, 1], [1, 0]], dtype=complex)
    h = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)
    custom = np.kron(x, h)
    op = qml.ctrl(qml.QubitUnitary, control=[0, 3])(custom, wires=[1, 2])
    return qml.tape.QuantumScript([op], [])
