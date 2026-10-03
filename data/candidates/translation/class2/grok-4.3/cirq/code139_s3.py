# EVAL_META: task_id=139, framework=cirq, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    arr = np.asarray(data)
    if arr.ndim == 2:
        eigvals, eigvecs = np.linalg.eigh(arr)
        idx = np.argmax(eigvals)
        state = eigvecs[:, idx]
    else:
        state = arr.ravel()
    n = int(np.log2(state.shape[0]))
    qargs_A = [q for q in range(n) if q not in qargs_B]
    tensor = state.reshape([2] * n)
    axes_A = [n - 1 - q for q in qargs_A]
    axes_B = [n - 1 - q for q in qargs_B]
    tensor = np.transpose(tensor, axes_A + axes_B)
    dimA = 2 ** len(qargs_A)
    dimB = 2 ** len(qargs_B)
    mat = tensor.reshape((dimA, dimB))
    U, S, Vh = np.linalg.svd(mat, full_matrices=False)
    result = []
    for i in range(len(S)):
        if abs(S[i]) > 1e-9:
            result.append((S[i], U[:, i], Vh[i, :]))
    return result
