# EVAL_META: task_id=139, framework=pennylane, class=2
import numpy as np
import pennylane as qml

def schmidt_test(data, qargs_B):
    arr = np.asarray(data)
    if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
        raise ValueError("Input data must be a square matrix representing a state vector or density matrix.")
    dim = arr.shape[0]
    n = int(round(np.log2(dim)))
    if 2**n != dim:
        raise ValueError("Dimension must be a power of 2.")
    qargs_B = list(qargs_B)
    all_wires = list(range(n))
    qargs_A = [w for w in all_wires if w not in qargs_B]
    perm = qargs_A + qargs_B
    dims = [2] * n

    if np.allclose(arr @ arr, arr, atol=1e-8) and np.allclose(np.trace(arr), 1.0, atol=1e-8):
        evals, evecs = np.linalg.eigh(arr)
        idx = int(np.argmax(np.real(evals)))
        state = evecs[:, idx]
    else:
        evals, evecs = np.linalg.eigh(arr)
        idx = int(np.argmax(np.real(evals)))
        state = evecs[:, idx]

    state_t = np.reshape(state, dims)
    state_t = np.transpose(state_t, perm)
    dim_a = 2 ** len(qargs_A)
    dim_b = 2 ** len(qargs_B)
    mat = np.reshape(state_t, (dim_a, dim_b))

    U, S, Vh = np.linalg.svd(mat, full_matrices=False)
    terms = []
    tol = 1e-12
    for i, s in enumerate(S):
        if s > tol:
            vec_a = U[:, i]
            vec_b = np.conjugate(Vh[i, :])
            terms.append((s, vec_a, vec_b))
    return terms
