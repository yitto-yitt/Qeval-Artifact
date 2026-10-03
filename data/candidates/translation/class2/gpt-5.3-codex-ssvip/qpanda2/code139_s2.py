# EVAL_META: task_id=139, framework=qpanda2, class=2
import numpy as np
import pyqpanda as pq


def schmidt_test(data, qargs_B):
    arr = np.asarray(data, dtype=complex)
    if arr.ndim == 1:
        dim = arr.size
        n = int(round(np.log2(dim)))
        if 2 ** n != dim:
            raise ValueError("Statevector length must be a power of 2.")
        psi = arr.reshape([2] * n)
    elif arr.ndim == 2:
        if arr.shape[0] != arr.shape[1]:
            raise ValueError("Density matrix must be square.")
        dim = arr.shape[0]
        n = int(round(np.log2(dim)))
        if 2 ** n != dim:
            raise ValueError("Density matrix dimension must be a power of 2.")
        vals, vecs = np.linalg.eigh(arr)
        idx = int(np.argmax(np.real(vals)))
        state = vecs[:, idx]
        norm = np.linalg.norm(state)
        if norm == 0:
            raise ValueError("Invalid density matrix.")
        state = state / norm
        psi = state.reshape([2] * n)
    else:
        raise ValueError("Input data must be a statevector or density matrix.")

    qargs_B = list(qargs_B)
    n = psi.ndim
    all_idx = list(range(n))
    qargs_A = [i for i in all_idx if i not in qargs_B]

    perm = qargs_A + qargs_B
    psi_perm = np.transpose(psi, axes=perm)

    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    mat = psi_perm.reshape(dim_A, dim_B)

    U, S, Vh = np.linalg.svd(mat, full_matrices=False)

    terms = []
    tol = 1e-12
    for k, coeff in enumerate(S):
        if coeff > tol:
            vec_A = U[:, k]
            vec_B = np.conjugate(Vh[k, :])
            terms.append((float(np.real_if_close(coeff)), vec_A, vec_B))
    return terms
