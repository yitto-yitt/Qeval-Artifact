# EVAL_META: task_id=139, framework=qpanda2, class=2
import numpy as np
import pyqpanda as pq

def schmidt_test(data, qargs_B):
    # Convert data to a statevector if necessary
    if hasattr(data, 'data'):
        data = data.data
    data = np.asarray(data)
    if data.ndim == 2:
        # Density matrix: check purity and extract statevector
        if data.shape[0] != data.shape[1]:
            raise ValueError("Data must be a square matrix or a statevector.")
        n = int(np.log2(data.shape[0]))
        eigvals, eigvecs = np.linalg.eigh(data)
        idx = np.argmax(np.abs(eigvals))
        if not np.isclose(eigvals[idx], 1.0) or not np.allclose(np.delete(eigvals, idx), 0.0, atol=1e-8):
            raise ValueError("Input density matrix is not a pure state.")
        state = eigvecs[:, idx]
    else:
        state = data.flatten()
        n = int(np.log2(state.shape[0]))

    qargs_B = list(qargs_B)
    qargs_A = [i for i in range(n) if i not in qargs_B]

    # Reshape to tensor and transpose to group A then B
    tensor = state.reshape([2] * n)
    perm = qargs_A + qargs_B
    tensor = np.transpose(tensor, axes=perm)
    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    matrix = tensor.reshape((dim_A, dim_B))

    # Singular value decomposition
    U, S, Vh = np.linalg.svd(matrix, full_matrices=False)

    result = []
    for i in range(len(S)):
        if S[i] < 1e-12:
            continue
        coeff = S[i]
        state_A = U[:, i]
        state_B = Vh[i, :].conj()
        result.append((coeff, state_A, state_B))
    return result
