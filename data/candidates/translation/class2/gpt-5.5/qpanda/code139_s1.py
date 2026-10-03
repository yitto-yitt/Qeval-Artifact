# EVAL_META: task_id=139, framework=qpanda, class=2
import numpy as np
import pyqpanda3.core as pq

def schmidt_test(data, qargs_B):
    arr = np.asarray(getattr(data, "data", data), dtype=complex)

    if arr.ndim == 2:
        if arr.shape[0] == arr.shape[1]:
            vals, vecs = np.linalg.eigh(arr)
            idx = int(np.argmax(vals.real))
            arr = vecs[:, idx] * np.sqrt(max(vals[idx].real, 0.0))
        else:
            arr = arr.reshape(-1)
    else:
        arr = arr.reshape(-1)

    dim = arr.size
    n = int(round(np.log2(dim)))
    if 2 ** n != dim:
        raise ValueError("Input state dimension is not a power of 2.")

    qargs_B = list(qargs_B)
    qargs_A = [q for q in range(n) if q not in qargs_B]

    dims = [2] * n
    tensor = arr.reshape(dims)

    axes_A = [n - 1 - q for q in reversed(qargs_A)]
    axes_B = [n - 1 - q for q in reversed(qargs_B)]
    tensor = np.transpose(tensor, axes_A + axes_B)

    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    matrix = tensor.reshape(dim_A, dim_B)

    u, s, vh = np.linalg.svd(matrix, full_matrices=False)

    if s.size == 0:
        return []

    tol = max(matrix.shape) * np.finfo(float).eps * float(np.max(s))
    result = []
    for i, coeff in enumerate(s):
        if coeff > tol:
            result.append((float(coeff), np.array(u[:, i], dtype=complex), np.array(vh[i, :], dtype=complex)))
    return result
