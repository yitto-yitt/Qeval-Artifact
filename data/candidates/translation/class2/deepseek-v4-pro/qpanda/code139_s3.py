# EVAL_META: task_id=139, framework=qpanda, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    arr = np.asarray(data)
    if arr.ndim == 1:
        psi = arr.astype(np.complex128)
    elif arr.ndim == 2:
        if arr.shape[0] != arr.shape[1]:
            raise ValueError("Density matrix must be square")
        eigvals, eigvecs = np.linalg.eigh(arr)
        idx = int(np.argmax(eigvals))
        psi = eigvecs[:, idx]
    else:
        raise ValueError("Input must be a 1D state vector or 2D density matrix")

    n = int(np.log2(psi.shape[0]))
    if 2 ** n != psi.shape[0]:
        raise ValueError("Dimension must be a power of 2")

    if isinstance(qargs_B, (int, np.integer)):
        qargs_B = [int(qargs_B)]
    else:
        qargs_B = sorted([int(q) for q in qargs_B])

    qargs_big = sorted(n - 1 - q for q in qargs_B)
    A_axes = [i for i in range(n) if i not in qargs_big]
    order = A_axes + qargs_big

    psi_tensor = psi.reshape((2,) * n)
    psi_tensor = psi_tensor.transpose(order)
    dim_A = 2 ** len(A_axes)
    dim_B = 2 ** len(qargs_big)
    mat = psi_tensor.reshape((dim_A, dim_B))

    U, s, Vh = np.linalg.svd(mat, full_matrices=False)

    return [(float(s[i]), U[:, i], Vh[i, :]) for i in range(len(s))]
