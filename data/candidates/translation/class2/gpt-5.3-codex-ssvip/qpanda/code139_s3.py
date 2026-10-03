# EVAL_META: task_id=139, framework=qpanda, class=2
import numpy as np
from pyqpanda3.core import *

def schmidt_test(data, qargs_B):
    arr = np.asarray(data, dtype=complex)
    if arr.ndim == 2:
        vals, vecs = np.linalg.eigh(arr)
        idx = int(np.argmax(vals.real))
        state = vecs[:, idx]
    else:
        state = arr.reshape(-1)

    n = int(round(np.log2(state.size)))
    qargs_B = list(qargs_B)
    qargs_A = [i for i in range(n) if i not in qargs_B]

    perm = qargs_A + qargs_B
    tensor = state.reshape([2] * n)
    tensor_perm = np.transpose(tensor, axes=perm)

    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    mat = tensor_perm.reshape(dim_A, dim_B)

    U, S, Vh = np.linalg.svd(mat, full_matrices=False)

    terms = []
    for i, s in enumerate(S):
        if np.abs(s) > 1e-12:
            terms.append((s, U[:, i], Vh[i, :].conj()))
    return terms
