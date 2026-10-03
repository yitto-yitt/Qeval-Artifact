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
    k = len(qargs)
    result = np.zeros((2**n, 2**n), dtype=complex)

    for in_idx in range(2**n):
        in_bits = [(in_idx >> i) & 1 for i in range(n)]
        sub_in = 0
        for t, q in enumerate(qargs):
            sub_in |= (in_bits[q] << t)

        for sub_out in range(2**k):
            amp = yx[sub_out, sub_in]
            if amp == 0:
                continue
            out_bits = in_bits.copy()
            for t, q in enumerate(qargs):
                out_bits[q] = (sub_out >> t) & 1
            out_idx = sum((out_bits[i] << i) for i in range(n))
            result[out_idx, in_idx] += amp

    return result
