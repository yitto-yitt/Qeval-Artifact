# EVAL_META: task_id=139, framework=qpanda, class=2
from pyqpanda3.core import *
import numpy as np
def schmidt_test(data, qargs_B):
    mat = np.asarray(data)
    if mat.ndim == 1:
        n = int(np.log2(len(mat)))
        dims = [2] * n
        b_dims = [dims[i] for i in qargs_B]
        a_dims = [d for i, d in enumerate(dims) if i not in qargs_B]
        mat = mat.reshape(list(reversed(a_dims + b_dims)))
        mat = mat.transpose()
    u, s, vh = np.linalg.svd(mat, full_matrices=False)
    terms = []
    for i, coeff in enumerate(s):
        if abs(coeff) < 1e-10:
            continue
        vec_a = u[:, i]
        vec_b = vh[i, :]
        terms.append((coeff, vec_a, vec_b))
    return terms
