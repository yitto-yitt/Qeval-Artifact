# EVAL_META: task_id=139, framework=qpanda2, class=2
import numpy as np
import pyqpanda as pq


def schmidt_test(data, qargs_B):
    arr = np.asarray(data, dtype=complex)
    if arr.ndim == 1:
        n = int(round(np.log2(arr.size)))
        if 2 ** n != arr.size:
            raise ValueError("Statevector length must be a power of 2.")
        psi = arr.reshape([2] * n)
    elif arr.ndim == 2:
        if arr.shape[0] != arr.shape[1]:
            raise ValueError("Density matrix must be square.")
        vals, vecs = np.linalg.eigh(arr)
        idx = int(np.argmax(np.real(vals)))
        state = vecs[:, idx]
        n = int(round(np.log2(state.size)))
        if 2 ** n != state.size:
            raise ValueError("State dimension must be a power of 2.")
        psi = state.reshape([2] * n)
    else:
        raise ValueError("Input data must be a statevector or density matrix.")

    n = psi.ndim
    qargs_B = list(qargs_B)
    set_B = set(qargs_B)
    qargs_A = [i for i in range(n) if i not in set_B]

    perm = qargs_A + qargs_B
    psi_perm = np.transpose(psi, perm)

    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    mat = psi_perm.reshape(dim_A, dim_B)

    U, S, Vh = np.linalg.svd(mat, full_matrices=False)

    terms = []
    for i, coeff in enumerate(S):
        if np.abs(coeff) > 1e-12:
            state_A = U[:, i]
            state_B = np.conjugate(Vh[i, :])
            terms.append((coeff, state_A, state_B))
    return terms
