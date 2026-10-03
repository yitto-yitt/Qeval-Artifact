# EVAL_META: task_id=41, framework=cirq, class=3
import numpy as np
import cirq


def compose_op():
    identity = np.eye(2 ** 3)
    Y = cirq.unitary(cirq.Y)
    X = cirq.unitary(cirq.X)
    yx = np.kron(Y, X)

    full_yx = np.eye(8, dtype=complex)
    for i in range(8):
        for j in range(8):
            b2_i, b0_i = (i >> 1) & 1, i & 1
            mid_i = (i >> 2) & 1
            b2_j, b0_j = (j >> 1) & 1, j & 1
            mid_j = (j >> 2) & 1
            if mid_i != mid_j:
                full_yx[i, j] = 0
                continue
            row = b2_i * 2 + b0_i
            col = b2_j * 2 + b0_j
            full_yx[i, j] = yx[row, col]

    result = identity @ full_yx
    return result
