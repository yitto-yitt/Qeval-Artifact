# EVAL_META: task_id=41, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def compose_op():
    op = np.eye(2**3, dtype=complex)
    y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    x = np.array([[0, 1], [1, 0]], dtype=complex)
    yx = np.kron(y, x)

    full = np.zeros((8, 8), dtype=complex)
    for in_idx in range(8):
        b0 = (in_idx >> 0) & 1
        b1 = (in_idx >> 1) & 1
        b2 = (in_idx >> 2) & 1
        col = (b0 << 1) | b2
        for out_col in range(4):
            ob0 = (out_col >> 1) & 1
            ob2 = out_col & 1
            out_idx = (ob0 << 0) | (b1 << 1) | (ob2 << 2)
            full[out_idx, in_idx] = yx[out_col, col]

    return full @ op
