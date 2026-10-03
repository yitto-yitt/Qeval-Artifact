# EVAL_META: task_id=139, framework=pennylane, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    arr = np.asarray(data)

    if arr.ndim == 2:
        rho = arr
        if rho.shape[0] != rho.shape[1]:
            raise ValueError("Density matrix must be square")
        d = rho.shape[0]
        n = int(np.log2(d))
        if 2 ** n != d:
            raise ValueError("Density matrix dimension must be a power of 2")

        evals, evecs = np.linalg.eigh(rho)
        idx = int(np.argmax(evals))
        if not np.isclose(evals[idx], 1.0, atol=1e-8):
            raise ValueError("Schmidt decomposition requires a pure state density matrix")
        psi = evecs[:, idx]

    elif arr.ndim == 1:
        psi = arr
        d = psi.shape[0]
        n = int(np.log2(d))
        if 2 ** n != d:
            raise ValueError("State vector dimension must be a power of 2")
    else:
        raise ValueError("Input must be a state vector or density matrix")

    if isinstance(qargs_B, (int, np.integer)):
        qargs_B = [int(qargs_B)]
    else:
        qargs_B = [int(q) for q in qargs_B]

    if len(qargs_B) == 0 or len(qargs_B) >= n:
        raise ValueError("qargs_B must be a non-empty proper subset of qubit indices")
    if len(set(qargs_B)) != len(qargs_B) or any(q < 0 or q >= n for q in qargs_B):
        raise ValueError("qargs_B contains invalid qubit indices")

    qargs_A = [q for q in range(n) if q not in qargs_B]
    axes = qargs_A + qargs_B

    tensor = psi.reshape([2] * n)
    tensor = np.transpose(tensor, axes=axes)

    dim_a = 2 ** len(qargs_A)
    dim_b = 2 ** len(qargs_B)
    matrix = tensor.reshape(dim_a, dim_b)

    u, s, vh = np.linalg.svd(matrix, full_matrices=False)

    terms = []
    atol = 1e-12
    for i, coeff in enumerate(s):
        if coeff > atol:
            terms.append((float(coeff), u[:, i], vh[i, :]))

    return terms
