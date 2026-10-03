# EVAL_META: task_id=139, framework=pennylane, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    data = np.asarray(data)
    if data.ndim == 2:
        u, s, vh = np.linalg.svd(data)
        vec = u[:, 0]
    else:
        vec = data
    n = int(np.log2(len(vec)))
    if isinstance(qargs_B, int):
        qargs_B = [qargs_B]
    qargs_A = [i for i in range(n) if i not in qargs_B]
    vec = vec.reshape([2] * n)
    vec = np.transpose(vec, qargs_A + qargs_B)
    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    mat = vec.reshape(dim_A, dim_B)
    u, s, vh = np.linalg.svd(mat)
    return [(s[i], u[:, i], vh[i].conj()) for i in range(len(s))]
