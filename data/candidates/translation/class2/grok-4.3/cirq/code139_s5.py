# EVAL_META: task_id=139, framework=cirq, class=2
import numpy as np
from math import log2

def schmidt_test(data, qargs_B):
    vec = np.asarray(data).ravel()
    n = int(log2(len(vec)))
    all_qubits = set(range(n))
    qargs_A = sorted(all_qubits - set(qargs_B))
    nB = len(qargs_B)
    nA = len(qargs_A)
    dimA = 1 << nA
    dimB = 1 << nB
    order = qargs_A + qargs_B
    idx = np.arange(1 << n).reshape([2] * n)
    idx = np.transpose(idx, order).reshape(dimA, dimB)
    mat = vec[idx]
    U, S, Vh = np.linalg.svd(mat, full_matrices=False)
    terms = []
    for i, s in enumerate(S):
        if abs(s) < 1e-12:
            continue
        u = U[:, i]
        v = Vh[i, :]
        terms.append((s, u, v))
    return terms
