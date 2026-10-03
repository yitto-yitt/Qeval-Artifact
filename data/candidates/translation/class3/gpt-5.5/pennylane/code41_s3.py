# EVAL_META: task_id=41, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def compose_op():
    x = np.array([[0, 1], [1, 0]], dtype=complex)
    y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    identity = np.eye(2, dtype=complex)
    matrix = np.kron(np.kron(y, identity), x)
    return qml.QubitUnitary(matrix, wires=[0, 1, 2])
