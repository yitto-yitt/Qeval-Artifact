# EVAL_META: task_id=139, framework=qpanda2, class=2
import numpy as np
from numpy.linalg import svd
def schmidt_test(data, qargs_B):
    vec = np.asarray(data, dtype=complex).ravel()
    n = int(np.log2(vec.size))
    nb = len(qargs_B)
    na = n - nb
    dim_a = 2 ** na
    dim_b = 2 ** nb
    mat = vec.reshape((dim_a, dim_b))
    U, S, Vh = svd(mat, full_matrices=False)
    terms = []
    for s, ua, vb in zip(S, U.T, Vh):
        if abs(s) > 1e-12:
            terms.append((float(s), ua, vb))
    return terms
