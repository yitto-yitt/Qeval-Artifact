# EVAL_META: task_id=139, framework=pennylane, class=2
import numpy as np


def schmidt_test(data, qargs_B):
    data = np.asarray(data)

    if data.ndim == 1:
        vector = data
        dim = vector.shape[0]
        n = int(np.log2(dim))
        if 2 ** n != dim:
            raise ValueError("Input vector dimension must be a power of 2")
    elif data.ndim == 2 and data.shape[0] == data.shape[1]:
        rho = data
        dim = rho.shape[0]
        n = int(np.log2(dim))
        if 2 ** n != dim:
            raise ValueError("Input density matrix dimension must be a power of 2")

        eigvals, eigvecs = np.linalg.eigh(rho)
        max_idx = int(np.argmax(eigvals))
        if not np.isclose(eigvals[max_idx], 1.0, atol=1e-10):
            raise ValueError("Schmidt decomposition is only defined for pure states")
        vector = eigvecs[:, max_idx]
    else:
        raise ValueError("Input must be a state vector or density matrix")

    qargs_B = [int(q) for q in qargs_B]

    if len(qargs_B) == 0 or len(qargs_B) >= n:
        raise ValueError("qargs_B must select a non-empty strict subsystem")
    if any(q < 0 or q >= n for q in qargs_B):
        raise ValueError("qargs_B contains an invalid qubit index")
    if len(set(qargs_B)) != len(qargs_B):
        raise ValueError("qargs_B contains duplicate qubit indices")

    qargs_A = [q for q in range(n) if q not in set(qargs_B)]

    tensor = vector.reshape((2,) * n)
    axes = [n - 1 - q for q in qargs_A] + [n - 1 - q for q in qargs_B]
    tensor = np.transpose(tensor, axes)

    dim_a = 2 ** len(qargs_A)
    dim_b = 2 ** len(qargs_B)
    matrix = tensor.reshape((dim_a, dim_b))

    u, s, vh = np.linalg.svd(matrix, full_matrices=False)

    terms = []
    for i in range(len(s)):
        vec_a = u[:, i]
        vec_b = np.conj(vh[i])
        terms.append((float(s[i]), vec_a, vec_b))

    return terms
