# EVAL_META: task_id=139, framework=qpanda2, class=2
import numpy as np
from pyqpanda import *
def schmidt_test(data, qargs_B):
    vec = np.asarray(data).ravel()
    n = int(np.log2(len(vec)))
    nb = len(qargs_B)
    na = n - nb
    dims = [2] * n
    axes = list(range(n))
    for i, q in enumerate(qargs_B):
        axes.remove(q)
        axes.append(q)
    vec = vec.reshape(dims).transpose(axes).reshape(2**na, 2**nb)
    u, s, vh = np.linalg.svd(vec, full_matrices=False)
    terms = []
    for i in range(len(s)):
        if s[i] > 1e-10:
            coeff = s[i]
            va = u[:, i]
            vb = vh[i, :]
            terms.append((coeff, va, vb))
    return terms
