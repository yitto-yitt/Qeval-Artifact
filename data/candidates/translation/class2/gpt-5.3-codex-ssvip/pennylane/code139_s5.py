# EVAL_META: task_id=139, framework=pennylane, class=2
import numpy as np
import pennylane as qml

def schmidt_test(data, qargs_B):
    arr = np.asarray(data, dtype=complex)
    if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
        raise ValueError("Input data must be a square matrix.")
    dim = arr.shape[0]
    n = int(round(np.log2(dim)))
    if 2**n != dim:
        raise ValueError("Input dimension must be a power of 2.")

    qargs_B = list(qargs_B)
    all_wires = list(range(n))
    qargs_A = [w for w in all_wires if w not in qargs_B]

    rho = qml.math.asarray(arr)
    evals, evecs = np.linalg.eigh(np.asarray(rho))
    idx = int(np.argmax(evals.real))
    psi = evecs[:, idx]
    psi = psi / np.linalg.norm(psi)

    tensor = psi.reshape([2] * n)
    perm = qargs_A + qargs_B
    tensor_perm = np.transpose(tensor, axes=perm)

    dimA = 2 ** len(qargs_A)
    dimB = 2 ** len(qargs_B)
    mat = tensor_perm.reshape(dimA, dimB)

    U, S, Vh = np.linalg.svd(mat, full_matrices=False)

    terms = []
    tol = 1e-12
    for i, s in enumerate(S):
        if s > tol:
            a_state = U[:, i]
            b_state = np.conjugate(Vh[i, :])
            terms.append((s, a_state, b_state))
    return terms
