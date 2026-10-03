# EVAL_META: task_id=41, framework=cirq, class=3
import numpy as np


def compose_op():
    I2 = np.eye(2)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    yx = np.kron(Y, X)

    op = np.eye(2 ** 3, dtype=complex)

    embedded = np.zeros((8, 8), dtype=complex)
    for i in range(8):
        for j in range(8):
            b2 = (i >> 2) & 1
            b1 = (i >> 1) & 1
            b0 = i & 1
            c2 = (j >> 2) & 1
            c1 = (j >> 1) & 1
            c0 = j & 1
            if b1 == c1:
                yx_row = (b2 << 1) | b0
                yx_col = (c2 << 1) | c0
                embedded[i, j] = yx[yx_row, yx_col]

    return embedded @ op
