# EVAL_META: task_id=139, framework=qpanda2, class=2
import numpy as np
import pyqpanda as pq


def schmidt_test(data, qargs_B):
    arr = np.asarray(data, dtype=complex)
    if arr.ndim == 1:
        n = int(round(np.log2(arr.size)))
        if 2 ** n != arr.size:
            raise ValueError("Statevector length must be a power of 2.")
        state = arr
    elif arr.ndim == 2:
        if arr.shape[0] != arr.shape[1]:
            raise ValueError("Density matrix must be square.")
        n = int(round(np.log2(arr.shape[0])))
        if 2 ** n != arr.shape[0]:
            raise ValueError("Matrix dimension must be a power of 2.")
        vals, vecs = np.linalg.eigh(arr)
        idx = np.argmax(vals.real)
        state = vecs[:, idx]
        norm = np.linalg.norm(state)
        if norm == 0:
            raise ValueError("Invalid density matrix: dominant eigenvector has zero norm.")
        state = state / norm
    else:
        raise ValueError("Input data must be a statevector or density matrix.")

    all_qubits = list(range(n))
    qargs_B = list(qargs_B)
    set_B = set(qargs_B)
    if len(set_B) != len(qargs_B):
        raise ValueError("qargs_B contains duplicates.")
    if any((q < 0 or q >= n) for q in qargs_B):
        raise ValueError("qargs_B contains out-of-range qubit index.")

    qargs_A = [q for q in all_qubits if q not in set_B]
    perm = qargs_A + qargs_B

    tensor = state.reshape([2] * n)
    tensor_perm = np.transpose(tensor, perm)
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
