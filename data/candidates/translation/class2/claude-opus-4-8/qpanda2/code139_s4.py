# EVAL_META: task_id=139, framework=qpanda2, class=2
import numpy as np


def schmidt_test(data, qargs_B):
    sv = np.asarray(data, dtype=complex).ravel()
    total_qubits = int(round(np.log2(sv.size)))

    qargs_B = sorted(int(q) for q in qargs_B)
    qargs_A = [q for q in range(total_qubits) if q not in qargs_B]

    nA = len(qargs_A)
    nB = len(qargs_B)

    dimA = 2 ** nA
    dimB = 2 ** nB

    M = np.zeros((dimA, dimB), dtype=complex)

    for idx in range(sv.size):
        bits = [(idx >> (total_qubits - 1 - k)) & 1 for k in range(total_qubits)]

        a_index = 0
        for q in qargs_A:
            a_index = (a_index << 1) | bits[total_qubits - 1 - q]

        b_index = 0
        for q in qargs_B:
            b_index = (b_index << 1) | bits[total_qubits - 1 - q]

        M[a_index, b_index] = sv[idx]

    U, S, Vh = np.linalg.svd(M)

    terms = []
    for i in range(len(S)):
        coeff = S[i]
        if coeff <= 1e-12:
            continue
        vecA = U[:, i]
        vecB = Vh[i, :]
        terms.append((coeff, vecA, vecB))

    return terms
