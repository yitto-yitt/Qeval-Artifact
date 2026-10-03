# EVAL_META: task_id=41, framework=qpanda, class=3
import numpy as np

def compose_op():
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    I = np.eye(2, dtype=complex)
    return np.kron(Y, np.kron(I, X))
