# EVAL_META: task_id=139, framework=pennylane, class=2
import pennylane as qml
import numpy as np

def schmidt_test(data, qargs_B):
    n = int(np.log2(len(data)))
    nB = len(qargs_B)
    nA = n - nB
    tensor = np.reshape(data, [2] * n)
    axes_B = [n - 1 - q for q in qargs_B]
    axes_A = [n - 1 - q for q in range(n) if q not in qargs_B]
    new_axes = axes_A + axes_B
    tensor = np.transpose(tensor, new_axes)
    mat = tensor.reshape(2**nA, 2**nB)
    U, S, Vh = np.linalg.svd(mat, full_matrices=False)
    terms = []
    for i in range(len(S)):
        if S[i] > 1e-10:
            coeff = S[i]
            vecA = U[:, i]
            vecB = Vh[i].conj()
            terms.append((coeff, vecA, vecB))
    return terms
