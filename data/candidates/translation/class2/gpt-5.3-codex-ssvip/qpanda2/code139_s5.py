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
        n = int(round(np.log2(arr.shape[0])))
        if 2 ** n != arr.shape[0]:
            raise ValueError("Density matrix dimension must be a power of 2.")
        vals, vecs = np.linalg.eigh(arr)
        idx = int(np.argmax(np.real(vals)))
        state = vecs[:, idx]
        norm = np.linalg.norm(state)
        if norm == 0:
            raise ValueError("Invalid density matrix: dominant eigenvector has zero norm.")
        psi = (state / norm).reshape([2] * n)
    else:
        raise ValueError("Input data must be a statevector or density matrix.")

    qargs_B = list(qargs_B)
    n = psi.ndim
    all_qargs = list(range(n))
    qargs_A = [i for i in all_qargs if i not in qargs_B]
    perm = qargs_A + qargs_B
    psi_perm = np.transpose(psi, axes=perm)

    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    mat = psi_perm.reshape(dim_A, dim_B)

    U, S, Vh = np.linalg.svd(mat, full_matrices=False)
    terms = []
    for i, s in enumerate(S):
        if np.isclose(s, 0.0):
            continue
        vec_A = U[:, i]
        vec_B = np.conjugate(Vh[i, :])
        terms.append((s, vec_A, vec_B))
    return terms
