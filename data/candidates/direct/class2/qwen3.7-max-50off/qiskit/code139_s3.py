# EVAL_META: task_id=139, framework=qiskit, class=2
import numpy as np


def schmidt_test(data, qargs_B):
    data = np.array(data, dtype=complex)
    qargs_B = list(qargs_B)

    n = int(np.round(np.log2(data.shape[0])))

    # Extract pure state from density matrix
    if data.ndim == 2:
        eigenvalues, eigenvectors = np.linalg.eigh(data)
        idx = np.argmax(eigenvalues)
        state = eigenvectors[:, idx]
    else:
        state = data.copy()

    qargs_A = [i for i in range(n) if i not in qargs_B]
    n_A = len(qargs_A)
    n_B = len(qargs_B)

    # Permute qubits: B qubits to LSB positions, A qubits to MSB positions
    new_order = qargs_B + qargs_A

    indices = np.arange(2**n)
    new_indices = np.zeros(2**n, dtype=int)
    for k in range(n):
        new_indices |= ((indices >> new_order[k]) & 1) << k

    new_state = np.zeros(2**n, dtype=complex)
    new_state[new_indices] = state

    # Reshape into matrix with A indexing rows and B indexing columns
    psi = new_state.reshape(2**n_A, 2**n_B)

    # SVD gives Schmidt decomposition
    U, S, Vh = np.linalg.svd(psi, full_matrices=False)

    terms = []
    for i in range(len(S)):
        if S[i] > 1e-10:
            terms.append((float(S[i]), U[:, i], Vh[i, :]))

    return terms
