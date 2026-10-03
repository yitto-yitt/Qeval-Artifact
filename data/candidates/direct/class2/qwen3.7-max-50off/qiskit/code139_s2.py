# EVAL_META: task_id=139, framework=qiskit, class=2
import numpy as np


def schmidt_test(data, qargs_B):
    if hasattr(data, 'to_matrix'):
        data = data.to_matrix()
    elif hasattr(data, 'data') and not isinstance(data, np.ndarray):
        data = data.data
    data = np.array(data, dtype=complex)

    if data.ndim == 1:
        psi = data
    elif data.ndim == 2:
        eigenvalues, eigenvectors = np.linalg.eigh(data)
        idx = np.argmax(np.real(eigenvalues))
        psi = eigenvectors[:, idx]
    else:
        raise ValueError("Invalid data format")

    n = int(round(np.log2(len(psi))))

    all_qubits = set(range(n))
    qargs_B_list = sorted([int(q) for q in qargs_B])
    qargs_B_set = set(qargs_B_list)
    qargs_A = sorted(all_qubits - qargs_B_set)

    tensor = psi.reshape([2] * n)

    axes_A = [n - 1 - q for q in qargs_A]
    axes_B = [n - 1 - q for q in qargs_B_list]

    perm = axes_A + axes_B
    tensor_t = np.transpose(tensor, perm)

    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B_list)
    matrix = tensor_t.reshape(dim_A, dim_B)

    U, S, Vh = np.linalg.svd(matrix, full_matrices=False)

    result = []
    for i in range(len(S)):
        if S[i] > 1e-10:
            coeff = float(S[i])
            state_A = U[:, i].copy()
            state_B = Vh[i, :].copy()
            result.append((coeff, state_A, state_B))

    return result
