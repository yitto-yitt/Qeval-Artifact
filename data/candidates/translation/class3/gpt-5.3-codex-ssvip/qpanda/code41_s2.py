# EVAL_META: task_id=41, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import matrix_decompose


def compose_op():
    op = np.eye(2**3, dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    yx = np.kron(Y, X)

    qargs = [0, 2]
    n = 3
    dim = 2**n
    full = np.zeros((dim, dim), dtype=complex)

    for col in range(dim):
        bits_in = [(col >> i) & 1 for i in range(n)]
        sub_in = bits_in[qargs[0]] + (bits_in[qargs[1]] << 1)
        for sub_out in range(4):
            amp = yx[sub_out, sub_in]
            if amp == 0:
                continue
            bits_out = bits_in.copy()
            bits_out[qargs[0]] = sub_out & 1
            bits_out[qargs[1]] = (sub_out >> 1) & 1
            row = sum((bits_out[i] << i) for i in range(n))
            full[row, col] += amp

    _ = matrix_decompose(full)
    return full
