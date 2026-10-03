# EVAL_META: task_id=139, framework=pennylane, class=2
import numpy as np
import pennylane as qml

def schmidt_test(data, qargs_B):
    arr = np.asarray(data)
    if arr.ndim == 1:
        state = arr.astype(complex)
    elif arr.ndim == 2 and arr.shape[1] == 1:
        state = arr[:, 0].astype(complex)
    elif arr.ndim == 2 and arr.shape[0] == arr.shape[1]:
        vals, vecs = np.linalg.eigh(arr.astype(complex))
        idx = int(np.argmax(np.real(vals)))
        state = vecs[:, idx]
    else:
        state = arr.reshape(-1).astype(complex)

    norm = np.linalg.norm(state)
    if norm == 0:
        raise ValueError("Input state has zero norm.")
    state = state / norm

    n = int(round(np.log2(state.size)))
    if 2**n != state.size:
        raise ValueError("State dimension must be a power of 2.")

    B = list(qargs_B)
    A = [i for i in range(n) if i not in B]

    perm = A + B
    tensor = state.reshape([2] * n)
    tensor_perm = np.transpose(tensor, axes=perm)

    dimA = 2 ** len(A)
    dimB = 2 ** len(B)
    mat = tensor_perm.reshape(dimA, dimB)

    U, S, Vh = np.linalg.svd(mat, full_matrices=False)

    terms = []
    tol = 1e-12
    for i, s in enumerate(S):
        if s > tol:
            terms.append((s, U[:, i], np.conjugate(Vh[i, :])))
    return terms
