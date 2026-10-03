# EVAL_META: task_id=139, framework=pennylane, class=2
import numpy as np


def schmidt_test(data, qargs_B):
    arr = np.asarray(data, dtype=complex)

    if arr.ndim == 2 and 1 in arr.shape:
        arr = arr.flatten()

    if arr.ndim == 1:
        vec = arr
        dim = vec.shape[0]
        if dim < 1 or (dim & (dim - 1)) != 0:
            raise ValueError("Statevector length must be a positive power of 2")
        num_qubits = int(np.log2(dim))
        norm = np.linalg.norm(vec)
        if norm < 1e-15:
            raise ValueError("Input statevector has zero norm")
        vec = vec / norm
    elif arr.ndim == 2:
        rho = arr
        if rho.shape[0] != rho.shape[1]:
            raise ValueError("Density matrix must be square")
        dim = rho.shape[0]
        if dim < 1 or (dim & (dim - 1)) != 0:
            raise ValueError("Density matrix dimension must be a positive power of 2")
        num_qubits = int(np.log2(dim))

        purity = np.trace(rho @ rho)
        if not np.isclose(np.real(purity), 1.0, rtol=1e-10, atol=1e-10):
            raise ValueError("Input density matrix is not pure")

        _, eigvecs = np.linalg.eigh(rho)
        vec = eigvecs[:, -1]
    else:
        raise ValueError("Input must be a statevector or density matrix")

    if isinstance(qargs_B, (int, np.integer)):
        qargs_B = [int(qargs_B)]
    else:
        qargs_B = [int(q) for q in qargs_B]

    if len(qargs_B) == 0:
        raise ValueError("qargs_B must be non-empty")
    if len(set(qargs_B)) != len(qargs_B):
        raise ValueError("qargs_B contains duplicate qubit indices")
    if any(q < 0 or q >= num_qubits for q in qargs_B):
        raise ValueError("qargs_B indices are out of range")

    qargs_A = [i for i in range(num_qubits) if i not in qargs_B]
    dims_A = 2 ** len(qargs_A)
    dims_B = 2 ** len(qargs_B)

    tensor = vec.reshape([2] * num_qubits)
    tensor = np.transpose(tensor, qargs_A + qargs_B)
    matrix = tensor.reshape(dims_A, dims_B)

    u, s, vh = np.linalg.svd(matrix, full_matrices=False)

    terms = []
    for i, coeff in enumerate(s):
        if not np.isclose(coeff, 0.0):
            state_A = u[:, i].reshape(dims_A)
            state_B = vh[i].conj().reshape(dims_B)
            terms.append((float(coeff), state_A, state_B))

    return terms
