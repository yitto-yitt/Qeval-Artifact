# EVAL_META: task_id=139, framework=qpanda2, class=2
import numpy as np
import pyqpanda as pq


def schmidt_test(data, qargs_B):
    arr = np.array(data, dtype=complex)
    if arr.ndim == 1:
        n = int(round(np.log2(arr.size)))
        if 2 ** n != arr.size:
            raise ValueError("Statevector length must be a power of 2.")
        psi = arr.reshape(-1)
    elif arr.ndim == 2:
        if arr.shape[0] != arr.shape[1]:
            raise ValueError("Density matrix must be square.")
        evals, evecs = np.linalg.eigh(arr)
        idx = int(np.argmax(evals.real))
        psi = evecs[:, idx]
        n = int(round(np.log2(psi.size)))
        if 2 ** n != psi.size:
            raise ValueError("Density matrix dimension must be 2^n.")
    else:
        raise ValueError("Input data must be a statevector or density matrix.")

    all_qubits = list(range(n))
    qargs_B = list(qargs_B)
    qargs_A = [q for q in all_qubits if q not in qargs_B]

    if len(qargs_A) == 0 or len(qargs_B) == 0:
        coeff = 1.0
        state_A = np.array([1.0 + 0.0j]) if len(qargs_A) == 0 else psi.copy()
        state_B = np.array([1.0 + 0.0j]) if len(qargs_B) == 0 else psi.copy()
        return [(coeff, state_A, state_B)]

    perm = qargs_A + qargs_B
    tensor = psi.reshape([2] * n)
    tensor_perm = np.transpose(tensor, axes=perm)
    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    mat = tensor_perm.reshape(dim_A, dim_B)

    U, S, Vh = np.linalg.svd(mat, full_matrices=False)
    terms = []
    tol = 1e-12
    for i, s in enumerate(S):
        if s > tol:
            vec_A = U[:, i]
            vec_B = np.conjugate(Vh[i, :])
            terms.append((float(np.real_if_close(s)), vec_A, vec_B))
    return terms
