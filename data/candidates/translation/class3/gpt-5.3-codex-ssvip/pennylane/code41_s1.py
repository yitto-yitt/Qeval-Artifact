# EVAL_META: task_id=41, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def compose_op():
    I = np.eye(2, dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)

    op = np.eye(2**3, dtype=complex)
    yx_on_0_2 = np.kron(Y, np.kron(I, X))
    return qml.operation.Operator(yx_on_0_2)
