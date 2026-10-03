# EVAL_META: task_id=41, framework=cirq, class=3
import numpy as np
import cirq

def compose_op():
    Y = np.array([[0, -1j], [1j, 0]])
    I = np.eye(2)
    X = np.array([[0, 1], [1, 0]])
    return np.kron(Y, np.kron(I, X))
