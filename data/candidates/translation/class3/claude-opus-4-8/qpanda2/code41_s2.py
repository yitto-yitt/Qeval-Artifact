# EVAL_META: task_id=41, framework=qpanda2, class=3
import numpy as np


def compose_op():
    I = np.eye(2, dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)

    yx = np.kron(Y, X)

    op = np.eye(2 ** 3, dtype=complex)

    dim = 2 ** 3
    n = 3
    qargs = [0, 2]

    result = np.zeros((dim, dim), dtype=complex)
    for i in range(dim):
        for j in range(dim):
            in_bits = [(j >> b) & 1 for b in range(n)]
            sub_in = 0
            for idx, q in enumerate(qargs):
                sub_in |= in_bits[q] << idx
            for sub_out in range(4):
                amp = yx[sub_out, sub_in]
                if amp == 0:
                    continue
                out_bits = list(in_bits)
                for idx, q in enumerate(qargs):
                    out_bits[q] = (sub_out >> idx) & 1
                out_state = 0
                for b in range(n):
                    out_state |= out_bits[b] << b
                result[out_state, j] += amp

    final = op @ result
    return final
