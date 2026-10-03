# EVAL_META: task_id=139, framework=qiskit, class=2
import numpy as np


def schmidt_test(data, qargs_B):
    if hasattr(data, 'data'):
        data = np.array(data.data)
    else:
        data = np.array(data)

    if data.ndim == 1:
        state = data.astype(complex)
    elif data.ndim == 2:
        if data.shape[0] == data.shape[1]:
            eigenvalues, eigenvectors = np.linalg.eigh(data)
            idx = np.argmax(np.real(eigenvalues))
            state = eigenvectors[:, idx]
        else:
            state = data.flatten().astype(complex)
    else:
        raise ValueError("Invalid data format")

    n = int(round(np.log2(len(state))))

    qargs_B = list(qargs_B)
    qargs_A = [i for i in range(n) if i not in qargs_B]

    nA = len(qargs_A)
    nB = len(qargs_B)

    tensor = state.reshape([2] * n)

    perm = [n - 1 - q for q in qargs_A] + [n - 1 - q for q in qargs_B]
    tensor = np.transpose(tensor, perm)

    matrix = tensor.reshape(2**nA, 2**nB)

    U, S, Vh = np.linalg.svd(matrix, full_matrices=False)

    result = []
    for i in range(len(S)):
        if abs(S[i]) > 1e-10:
            coeff = float(np.real(S[i]))
            state_A = U[:, i]
            state_B = Vh[i, :]
            result.append((coeff, state_A, state_B))

    return result
