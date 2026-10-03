# EVAL_META: task_id=41, framework=cirq, class=3
import numpy as np
import cirq


def compose_op():
    op = np.eye(2**3, dtype=complex)
    y = cirq.unitary(cirq.Y)
    x = cirq.unitary(cirq.X)
    yx = np.kron(y, x)
    qubits = [0, 2]
    n = 3
    dim = 2**n
    result = np.zeros((dim, dim), dtype=complex)

    for col in range(dim):
        bits_in = [(col >> (n - 1 - i)) & 1 for i in range(n)]
        sub_in = 0
        for q in qubits:
            sub_in = (sub_in << 1) | bits_in[q]

        for sub_out in range(2 ** len(qubits)):
            amp = yx[sub_out, sub_in]
            if amp == 0:
                continue
            bits_out = bits_in.copy()
            for j, q in enumerate(qubits):
                bits_out[q] = (sub_out >> (len(qubits) - 1 - j)) & 1
            row = 0
            for i in range(n):
                row = (row << 1) | bits_out[i]
            result[row, col] += amp

    return result
