# EVAL_META: task_id=41, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def compose_op():
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    I = np.eye(2, dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    mat = np.kron(X, np.kron(I, Y))
    return qml.QubitUnitary(mat, wires=[0, 1, 2])
