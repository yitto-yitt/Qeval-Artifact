# EVAL_META: task_id=139, framework=qpanda2, class=2
import pyqpanda as pq
import numpy as np
def schmidt_test(data, qargs_B):
    vec = np.asarray(data).ravel()
    n = int(np.log2(len(vec)))
    nb = len(qargs_B)
    na = n - nb
    dim_a = 1 << na
    dim_b = 1 << nb
    mat = vec.reshape((dim_a, dim_b))
    u, s, vh = np.linalg.svd(mat, full_matrices=False)
    terms = []
    for i in range(len(s)):
        if s[i] > 1e-10:
            terms.append((s[i], u[:, i], vh[i, :]))
    return terms
