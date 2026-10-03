# EVAL_META: task_id=139, framework=qpanda2, class=2
from pyqpanda import *
import numpy as np
def schmidt_test(data, qargs_B):
    mat = np.asarray(data)
    if mat.ndim == 1:
        vec = mat
    else:
        evals, evecs = np.linalg.eigh(mat)
        vec = evecs[:, np.argmax(evals)]
    n = int(np.log2(vec.shape[0]))
    nB = len(qargs_B)
    nA = n - nB
    dims = [2] * n
    tensor = vec.reshape(dims)
    axesA = [i for i in range(n) if i not in qargs_B]
    axesB = qargs_B
    perm = axesA + axesB
    matAB = np.transpose(tensor, perm).reshape(2**nA, 2**nB)
    U, S, Vh = np.linalg.svd(matAB, full_matrices=False)
    terms = []
    for i, s in enumerate(S):
        if abs(s) < 1e-10:
            continue
        vecA = U[:, i]
        vecB = Vh[i, :]
        terms.append((s, vecA, vecB))
    return terms
