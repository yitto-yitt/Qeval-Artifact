# EVAL_META: task_id=139, framework=qpanda, class=2
import numpy as np
from pyqpanda3.core import *
def schmidt_test(data, qargs_B):
    psi = np.asarray(data, dtype=complex).ravel()
    n = int(np.log2(psi.size))
    qb = sorted(qargs_B)
    qa = [q for q in range(n) if q not in qb]
    perm = qa + qb
    idx = np.arange(psi.size).reshape([2]*n)
    idx = np.transpose(idx, axes=list(np.argsort(perm)))
    psi_r = psi[idx.ravel()].reshape((2**len(qa), 2**len(qb)))
    U, S, Vh = np.linalg.svd(psi_r, full_matrices=False)
    terms = []
    for s, u, v in zip(S, U.T, Vh):
        if abs(s) > 1e-10:
            terms.append((float(s), u, v))
    return terms
