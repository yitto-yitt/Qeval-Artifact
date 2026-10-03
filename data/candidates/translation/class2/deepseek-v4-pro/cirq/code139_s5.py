# EVAL_META: task_id=139, framework=cirq, class=2

import numpy as np


def schmidt_test(data, qargs_B):
    arr = np.asarray(data, dtype=complex)

    if np.isscalar(qargs_B):
        qargs_B = [qargs_B]
    qargs_B = sorted(int(q) for q in qargs_B)

    if arr.ndim == 1:
        vec = arr
        dim = vec.shape[0]
    elif arr.ndim == 2:
        if arr.shape[0] != arr.shape[1]:
            raise ValueError("Density matrix must be square")
        dim = arr.shape[0]
        eigvals, eigvecs = np.linalg.eigh(arr)
        idx = int(np.argmax(np.real(eigvals)))
        vec = eigvecs[:, idx]
    else:
        raise ValueError("Input must be a state vector or density matrix")

    n = int(round(np.log2(dim)))
    if 2 ** n != dim:
        raise ValueError("Dimension must be a power of 2")

    if not (0 < len(qargs_B) < n):
        raise ValueError("qargs_B must be a non-empty proper subset of qubits")

    qargs_A = [i for i in range(n) if i not in qargs_B]

    psi_tensor = vec.reshape([2] * n)
    psi_perm = np.transpose(psi_tensor, axes=qargs_A + qargs_B)

    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)

    mat = psi_perm.reshape(dim_A, dim_B)
    U, s, Vh = np.linalg.svd(mat, full_matrices=False)

    return [(s[i], U[:, i], Vh[i, :]) for i in range(len(s))]
