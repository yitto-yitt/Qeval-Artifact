# EVAL_META: task_id=139, framework=cirq, class=2
import numpy as np
import cirq


def schmidt_test(data, qargs_B):
    arr = np.asarray(data, dtype=complex)
    if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
        raise ValueError("Input data must be a square matrix.")
    dim = arr.shape[0]
    n = int(round(np.log2(dim)))
    if 2**n != dim:
        raise ValueError("Matrix dimension must be a power of 2.")

    qargs_B = tuple(qargs_B)
    if any((q < 0 or q >= n) for q in qargs_B):
        raise ValueError("qargs_B contains invalid qubit indices.")
    if len(set(qargs_B)) != len(qargs_B):
        raise ValueError("qargs_B contains duplicate indices.")

    qargs_A = tuple(i for i in range(n) if i not in qargs_B)
    if len(qargs_A) == 0 or len(qargs_B) == 0:
        raise ValueError("Both subsystems A and B must be non-empty.")

    evals, evecs = np.linalg.eigh(arr)
    idx = int(np.argmax(evals.real))
    psi = evecs[:, idx]
    norm = np.linalg.norm(psi)
    if norm == 0:
        raise ValueError("Cannot extract statevector from zero eigenvector.")
    psi = psi / norm

    tensor = psi.reshape((2,) * n)
    perm = qargs_A + qargs_B
    tensor_perm = np.transpose(tensor, perm)
    dim_a = 2 ** len(qargs_A)
    dim_b = 2 ** len(qargs_B)
    mat = tensor_perm.reshape(dim_a, dim_b)

    u, s, vh = np.linalg.svd(mat, full_matrices=False)
    terms = []
    tol = 1e-12
    for i, coeff in enumerate(s):
        if coeff > tol:
            vec_a = u[:, i]
            vec_b = np.conjugate(vh[i, :])
            terms.append((coeff, vec_a, vec_b))
    return terms
