# EVAL_META: task_id=139, framework=qpanda2, class=2
import numpy as np
import pyqpanda as pq


def schmidt_test(data, qargs_B):
    state = np.asarray(data, dtype=complex).reshape(-1)
    n = int(np.log2(len(state)))
    if 2 ** n != len(state):
        raise ValueError("Input state is not a valid statevector length")

    qargs_B = list(qargs_B)
    if len(qargs_B) == 0 or len(qargs_B) == n:
        raise ValueError("qargs_B must be a nonempty proper subset of qubits")
    if not all(isinstance(q, (int, np.integer)) for q in qargs_B):
        raise TypeError("qargs_B must contain only integers")
    if len(set(qargs_B)) != len(qargs_B):
        raise ValueError("qargs_B must not contain duplicates")
    if any(q < 0 or q >= n for q in qargs_B):
        raise ValueError("qargs_B contains an invalid qubit index")

    qargs_A = [q for q in range(n) if q not in qargs_B]

    # Internal axes order follows [n-1, n-2, ..., 0].
    axes_A = [n - 1 - q for q in qargs_A]
    axes_B = [n - 1 - q for q in qargs_B]

    tensor = np.reshape(state, [2] * n)
    matrix = np.transpose(tensor, axes_A + axes_B)
    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    matrix = np.reshape(matrix, (dim_A, dim_B))

    U, S, Vh = np.linalg.svd(matrix, full_matrices=False)

    terms = []
    threshold = 1e-10
    for i, coeff in enumerate(S):
        if coeff > threshold:
            state_a = np.asarray(U[:, i], dtype=complex).ravel()
            state_b = np.asarray(Vh[i, :], dtype=complex).ravel()
            terms.append((coeff, state_a, state_b))

    return terms
