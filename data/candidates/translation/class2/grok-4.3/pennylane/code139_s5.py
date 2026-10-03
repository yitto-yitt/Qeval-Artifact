# EVAL_META: task_id=139, framework=pennylane, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    psi = np.array(data, dtype=complex).ravel()
    n = int(np.log2(len(psi)))
    tensor = psi.reshape([2] * n)
    qargs_B = list(qargs_B)
    qargs_A = [i for i in range(n) if i not in qargs_B]
    axes_order = qargs_A + qargs_B
    tensor = np.transpose(tensor, axes_order)
    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    mat = tensor.reshape(dim_A, dim_B)
    U, S, Vh = np.linalg.svd(mat, full_matrices=False)
    result = []
    for s, u, v in zip(S, U.T, Vh):
        if abs(s) > 1e-12:
            result.append((s, u, v))
    return result
