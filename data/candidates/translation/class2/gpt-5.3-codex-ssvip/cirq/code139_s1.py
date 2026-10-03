# EVAL_META: task_id=139, framework=cirq, class=2
import numpy as np
import cirq


def schmidt_test(data, qargs_B):
    arr = np.asarray(data, dtype=complex)
    if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
        raise ValueError("Input 'data' must be a square matrix.")
    dim = arr.shape[0]
    n = int(round(np.log2(dim)))
    if 2**n != dim:
        raise ValueError("Matrix dimension must be a power of 2 for qubit systems.")

    vals, vecs = np.linalg.eigh(arr)
    idx = int(np.argmax(vals.real))
    psi = vecs[:, idx]

    all_qargs = list(range(n))
    qargs_B = list(qargs_B)
    qargs_A = [q for q in all_qargs if q not in qargs_B]

    psi_tensor = psi.reshape((2,) * n)
    perm = qargs_A + qargs_B
    psi_perm = np.transpose(psi_tensor, axes=perm)

    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    psi_matrix = psi_perm.reshape(dim_A, dim_B)

    U, s, Vh = np.linalg.svd(psi_matrix, full_matrices=False)

    terms = []
    for i, coeff in enumerate(s):
        if np.isclose(coeff, 0.0):
            continue
        state_A = U[:, i]
        state_B = np.conjugate(Vh[i, :])
        terms.append((coeff, state_A, state_B))

    return terms
