# EVAL_META: task_id=139, framework=pennylane, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    state = np.asarray(data)
    n = int(np.log2(state.size))
    qargs = [n - 1 - i for i in qargs_B]
    state = state.reshape([2] * n)
    qargs_A = [i for i in range(n) if i not in qargs]
    perm = qargs_A + qargs
    state = np.transpose(state, perm)
    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs)
    state = state.reshape(dim_A, dim_B)
    u, s, vh = np.linalg.svd(state, full_matrices=False)
    result = []
    for i in range(len(s)):
        coeff = float(s[i])
        state_A = u[:, i]
        state_B = vh[i, :]
        result.append((coeff, state_A, state_B))
    return result
