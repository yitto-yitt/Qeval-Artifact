# EVAL_META: task_id=41, framework=cirq, class=3
import numpy as np
import cirq


def compose_op():
    op = np.eye(2**3, dtype=complex)
    y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    x = np.array([[0, 1], [1, 0]], dtype=complex)
    yx = np.kron(y, x)

    qargs = [0, 2]
    n = 3
    k = len(qargs)

    result = np.zeros((2**n, 2**n), dtype=complex)
    qargs_set = set(qargs)

    for in_idx in range(2**n):
        in_bits = [(in_idx >> (n - 1 - i)) & 1 for i in range(n)]
        sub_in = 0
        for q in qargs:
            sub_in = (sub_in << 1) | in_bits[q]

        for sub_out in range(2**k):
            amp = yx[sub_out, sub_in]
            if amp == 0:
                continue
            out_bits = in_bits.copy()
            for j, q in enumerate(qargs):
                out_bits[q] = (sub_out >> (k - 1 - j)) & 1

            out_idx = 0
            for b in out_bits:
                out_idx = (out_idx << 1) | b
            result[out_idx, in_idx] += amp

    return cirq.MatrixGate(result)
