# EVAL_META: task_id=41, framework=cirq, class=3
import numpy as np
import cirq


def compose_op():
    identity = np.eye(2 ** 3)
    Y = cirq.unitary(cirq.Y)
    X = cirq.unitary(cirq.X)
    yx = np.kron(Y, X)

    dim = 2 ** 3
    full_yx = np.zeros((dim, dim), dtype=complex)
    qargs = [0, 2]
    num_qubits = 3

    def index_map(i):
        bits = [(i >> b) & 1 for b in range(num_qubits)]
        sub = 0
        for pos, q in enumerate(qargs):
            sub |= bits[q] << pos
        return bits, sub

    for i in range(dim):
        bits_i, sub_i = index_map(i)
        for sub_j in range(2 ** len(qargs)):
            amp = yx[sub_j, sub_i]
            if amp == 0:
                continue
            bits_j = list(bits_i)
            for pos, q in enumerate(qargs):
                bits_j[q] = (sub_j >> pos) & 1
            j = 0
            for b in range(num_qubits):
                j |= bits_j[b] << b
            full_yx[j, i] += amp

    return identity @ full_yx
