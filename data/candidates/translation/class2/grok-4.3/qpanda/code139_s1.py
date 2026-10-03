# EVAL_META: task_id=139, framework=qpanda, class=2
import numpy as np
from pyqpanda3.core import *

def schmidt_test(data, qargs_B):
    if isinstance(data, np.ndarray) and data.ndim == 2:
        eigvals, eigvecs = np.linalg.eigh(data)
        idx = np.argmax(eigvals)
        state = eigvecs[:, idx]
    else:
        state = np.asarray(data).ravel()
    n = int(np.log2(len(state)))
    n_B = len(qargs_B)
    n_A = n - n_B
    dim_A = 1 << n_A
    dim_B = 1 << n_B
    state = state.reshape((dim_A, dim_B), order="F")
    U, S, Vh = np.linalg.svd(state, full_matrices=False)
    terms = []
    for s, u_col, vh_row in zip(S, U.T, Vh):
        if abs(s) > 1e-10:
            terms.append((float(s), u_col, vh_row.conj()))
    return terms
