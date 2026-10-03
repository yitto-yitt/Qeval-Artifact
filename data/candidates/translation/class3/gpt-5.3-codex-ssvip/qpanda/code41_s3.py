# EVAL_META: task_id=41, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import *

def compose_op():
    op = np.eye(2**3, dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    yx = np.kron(Y, X)

    qargs = [0, 2]
    n = 3
    k = 2
    result = np.zeros((2**n, 2**n), dtype=complex)

    for in_idx in range(2**n):
        bits_in = [(in_idx >> b) & 1 for b in range(n)]
        sub_in = 0
        for p, q in enumerate(qargs):
            sub_in |= bits_in[q] << p

        for sub_out in range(2**k):
            amp = yx[sub_out, sub_in]
            if amp == 0:
                continue
            bits_out = bits_in.copy()
            for p, q in enumerate(qargs):
                bits_out[q] = (sub_out >> p) & 1
            out_idx = sum((bits_out[b] << b) for b in range(n))
            result[out_idx, in_idx] += amp

    return result
