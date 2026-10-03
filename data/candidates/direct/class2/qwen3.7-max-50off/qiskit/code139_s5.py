# EVAL_META: task_id=139, framework=qiskit, class=2
import numpy as np


def schmidt_test(data, qargs_B):
    if hasattr(data, 'data'):
        data = np.array(data.data, dtype=complex)
    else:
        data = np.array(data, dtype=complex)

    if data.ndim == 2:
        eigenvalues, eigenvectors = np.linalg.eigh(data)
        idx = np.argmax(eigenvalues)
        state_vector = eigenvectors[:, idx]
        state_vector = state_vector / np.linalg.norm(state_vector)
    elif data.ndim == 1:
        state_vector = data.astype(complex)
    else:
        raise ValueError("Invalid data format")

    n = int(round(np.log2(len(state_vector))))

    qargs_B = sorted(list(qargs_B))
    qargs_A = sorted([q for q in range(n) if q not in qargs_B])
    n_A = len(qargs_A)
    n_B = len(qargs_B)

    tensor = state_vector.reshape((2,) * n)

    A_axes = [n - 1 - q for q in qargs_A]
    B_axes = [n - 1 - q for q in qargs_B]

    perm = A_axes + B_axes
    tensor = np.transpose(tensor, perm)

    matrix = tensor.reshape((2 ** n_A, 2 ** n_B))

    U, S, Vh = np.linalg.svd(matrix, full_matrices=False)

    result = []
    for i in range(len(S)):
        if abs(S[i]) > 1e-10:
            coeff = float(S[i])
            state_A = U[:, i]
            state_B = Vh[i, :]
            result.append((coeff, state_A, state_B))

    return result
