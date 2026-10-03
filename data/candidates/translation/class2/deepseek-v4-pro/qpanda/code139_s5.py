# EVAL_META: task_id=139, framework=qpanda, class=2
import numpy as np
import pyqpanda3.core as pq


def schmidt_test(data, qargs_B):
    if hasattr(data, 'data'):
        data = data.data
    data = np.asarray(data, dtype=complex)

    if data.ndim == 2 and 1 in data.shape:
        data = data.flatten()

    if data.ndim == 1:
        dim = data.shape[0]
        n = int(round(np.log2(dim)))
        if 2**n != dim:
            raise ValueError("State dimension must be a power of 2")
        psi = data
    elif data.ndim == 2:
        if data.shape[0] != data.shape[1]:
            raise ValueError("Density matrix must be square")
        dim = data.shape[0]
        n = int(round(np.log2(dim)))
        if 2**n != dim:
            raise ValueError("Density matrix dimension must be a power of 2")

        eigvals, eigvecs = np.linalg.eigh(data)
        idx = np.argmax(np.abs(eigvals))
        if not np.isclose(eigvals[idx], 1.0, atol=1e-8):
            raise ValueError("Input density matrix is not pure")
        psi = eigvecs[:, idx]
    else:
        raise ValueError("Invalid input state")

    if isinstance(qargs_B, (int, np.integer)):
        qargs_B = [qargs_B]
    else:
        qargs_B = list(qargs_B)

    if len(qargs_B) == 0:
        raise ValueError("At least one qubit must be in subsystem B")
    for q in qargs_B:
        if q < 0 or q >= n:
            raise ValueError("Invalid qubit index")

    qargs_B = sorted(set(qargs_B))
    qargs_A = sorted(set(range(n)) - set(qargs_B))

    if not qargs_A:
        raise ValueError("At least one qubit must be in subsystem A")

    dims = [2] * n
    axes = qargs_A + qargs_B
    mat = np.reshape(psi, dims).transpose(axes)

    a_dim = 2 ** len(qargs_A)
    b_dim = 2 ** len(qargs_B)
    mat = np.reshape(mat, (a_dim, b_dim))

    u, s, vh = np.linalg.svd(mat, full_matrices=False)

    terms = []
    for i, sv in enumerate(s):
        if not np.isclose(sv, 0.0, atol=1e-8):
            terms.append((float(sv), u[:, i], vh[i].conj()))

    return terms
