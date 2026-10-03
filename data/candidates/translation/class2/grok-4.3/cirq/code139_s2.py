# EVAL_META: task_id=139, framework=cirq, class=2
import cirq
import numpy as np

def schmidt_test(data, qargs_B):
    vec = np.asarray(data).ravel()
    n = int(np.log2(len(vec)))
    k = len(qargs_B)
    dim_b = 2 ** k
    dim_a = 2 ** (n - k)
    mat = vec.reshape((dim_a, dim_b))
    U, S, Vh = np.linalg.svd(mat, full_matrices=False)
    terms = []
    for s, u_col, v_row in zip(S, U.T, Vh):
        if abs(s) > 1e-12:
            terms.append((float(s), u_col, v_row))
    return terms
