# EVAL_META: task_id=139, framework=qpanda2, class=2
import numpy as np


def schmidt_test(data, qargs_B):
    sv = np.asarray(data, dtype=complex).ravel()
    n = int(round(np.log2(sv.size)))

    qargs_B = sorted(int(q) for q in qargs_B)
    qargs_A = [q for q in range(n) if q not in qargs_B]

    dimA = 1 << len(qargs_A)
    dimB = 1 << len(qargs_B)

    M = np.zeros((dimA, dimB), dtype=complex)
    for idx in range(sv.size):
        bits = [(idx >> (n - 1 - k)) & 1 for k in range(n)]
        a = 0
        for q in qargs_A:
            a = (a << 1) | bits[n - 1 - q]
        b = 0
        for q in qargs_B:
            b = (b << 1) | bits[n - 1 - q]
        M[a, b] = sv[idx]

    U, S, Vh = np.linalg.svd(M)

    terms = []
    for i in range(len(S)):
        coeff = S[i]
        if coeff <= 1e-12:
            continue
        stateA = U[:, i]
        stateB = Vh[i, :]
        terms.append((float(coeff), stateA, stateB))

    return terms
