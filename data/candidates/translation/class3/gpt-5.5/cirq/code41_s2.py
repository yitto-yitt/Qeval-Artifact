# EVAL_META: task_id=41, framework=cirq, class=3
import numpy as np
import cirq


def compose_op():
    x = np.array([[0, 1], [1, 0]], dtype=complex)
    y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    i = np.eye(2, dtype=complex)
    return cirq.MatrixGate(np.kron(np.kron(y, i), x))
