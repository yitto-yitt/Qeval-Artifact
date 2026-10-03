# EVAL_META: task_id=139, framework=qpanda2, class=2
import numpy as np
import pyqpanda as pq


def schmidt_test(data, qargs_B):
    arr = np.asarray(data, dtype=complex)

    if arr.ndim == 1:
        psi = arr
    elif arr.ndim == 2:
        evals, evecs = np.linalg.eigh(arr)
        if abs(evals[-2]) > 1e-10:
            raise ValueError("Input density matrix is not a pure state")
        psi = evecs[:, -1]
    else:
        raise ValueError("Input must be a statevector or a density matrix")

    dim = psi.shape[0]
    n = int(np.log2(dim))
    if 2 ** n != dim:
        raise ValueError("State dimension must be a power of 2")

    if isinstance(qargs_B, (int, np.integer)):
        qargs_B = [int(qargs_B)]
    else:
        qargs_B = list(qargs_B)

    if len(qargs_B) == 0 or len(qargs_B) == n:
        raise ValueError("qargs_B must be a non-empty proper subset of qubit indices")

    if len(set(qargs_B)) != len(qargs_B):
        raise ValueError("qargs_B contains duplicate qubit indices")

    if any(q < 0 or q >= n for q in qargs_B):
        raise ValueError("qargs_B contains an out-of-range qubit index")

    qargs_A = [q for q in range(n) if q not in set(qargs_B)]
    dimA = 1 << len(qargs_A)
    dimB = 1 << len(qargs_B)

    idx = np.arange(dim, dtype=int)
    a_idx = np.zeros(dim, dtype=int)
    b_idx = np.zeros(dim, dtype=int)

    for pos, q in enumerate(qargs_A):
        a_idx |= ((idx >> q) & 1) << pos

    for pos, q in enumerate(qargs_B):
        b_idx |= ((idx >> q) & 1) << pos

    M = np.zeros((dimA, dimB), dtype=complex)
    M[a_idx, b_idx] = psi

    U, S, Vh = np.linalg.svd(M, full_matrices=False)

    terms = []
    for i in range(len(S)):
        coeff = float(S[i])
        state_a = U[:, i].copy()
        state_b = Vh[i].conj().copy()
        terms.append((coeff, state_a, state_b))

    return terms
