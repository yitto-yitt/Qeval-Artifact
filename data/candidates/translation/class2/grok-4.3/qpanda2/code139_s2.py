# EVAL_META: task_id=139, framework=qpanda2, class=2
import pyqpanda as pq
import numpy as np
def schmidt_test(data, qargs_B):
    if hasattr(data, 'data'):
        mat = np.asarray(data.data)
    else:
        mat = np.asarray(data)
    if mat.ndim == 1:
        vec = mat
    else:
        evals, evecs = np.linalg.eigh(mat)
        idx = np.argmax(evals)
        vec = evecs[:, idx]
    n = int(np.log2(len(vec)))
    nB = len(qargs_B)
    nA = n - nB
    dims = [2] * n
    idx = list(range(n))
    for i, q in enumerate(qargs_B):
        idx[q] = nA + i
    vec = vec.reshape(dims).transpose(idx).reshape(2**nA, 2**nB)
    U, S, Vh = np.linalg.svd(vec, full_matrices=False)
    terms = []
    for i, s in enumerate(S):
        if abs(s) > 1e-10:
            va = U[:, i]
            vb = Vh[i, :]
            terms.append((s, va, vb))
    return terms
