# EVAL_META: task_id=139, framework=cirq, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    vec = np.asarray(data).ravel()
    n = int(np.log2(vec.size))
    qargs_A = [q for q in range(n) if q not in qargs_B]
    new_order = qargs_A + qargs_B
    tensor = vec.reshape([2] * n).transpose(new_order)
    dimA = 2 ** len(qargs_A)
    dimB = 2 ** len(qargs_B)
    mat = tensor.reshape((dimA, dimB))
    U, S, Vh = np.linalg.svd(mat, full_matrices=False)
    result = []
    for i, s in enumerate(S):
        if abs(s) < 1e-10:
            continue
        vecA = U[:, i]
        vecB = Vh[i, :]
        result.append((s, vecA, vecB))
    return result
