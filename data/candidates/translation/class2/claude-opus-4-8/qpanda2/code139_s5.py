# EVAL_META: task_id=139, framework=qpanda2, class=2
import numpy as np


def schmidt_test(data, qargs_B):
    sv = np.asarray(getattr(data, "data", data), dtype=complex).reshape(-1)
    n = int(round(np.log2(sv.size)))
    if (1 << n) != sv.size:
        raise ValueError("state vector length must be a power of 2")

    qargs_B = sorted(int(q) for q in qargs_B)
    qargs_A = [q for q in range(n) if q not in qargs_B]

    dimA = 1 << len(qargs_A)
    dimB = 1 << len(qargs_B)

    def bit(index, q):
        return (index >> q) & 1

    def compose(a_idx, b_idx):
        idx = 0
        for pos, q in enumerate(qargs_A):
            if (a_idx >> pos) & 1:
                idx |= (1 << q)
        for pos, q in enumerate(qargs_B):
            if (b_idx >> pos) & 1:
                idx |= (1 << q)
        return idx

    M = np.zeros((dimA, dimB), dtype=complex)
    for a in range(dimA):
        for b in range(dimB):
            M[a, b] = sv[compose(a, b)]

    U, S, Vh = np.linalg.svd(M)

    terms = []
    for k in range(len(S)):
        coeff = float(S[k])
        if coeff <= 1e-12:
            continue
        a_vec = U[:, k]
        b_vec = Vh[k, :]
        terms.append((coeff, a_vec, b_vec))

    return terms
