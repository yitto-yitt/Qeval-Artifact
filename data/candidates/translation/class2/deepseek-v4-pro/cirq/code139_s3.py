# EVAL_META: task_id=139, framework=cirq, class=2
import numpy as np


def schmidt_test(data, qargs_B):
    state = np.asarray(data)

    if state.ndim == 1:
        vec = state
    elif state.ndim == 2:
        rho = state
        if not np.isclose(np.trace(rho @ rho), 1.0, atol=1e-10):
            raise ValueError("Input density matrix is not pure")
        eigvals, eigvecs = np.linalg.eigh(rho)
        vec = eigvecs[:, -1]
    else:
        raise ValueError("Input must be a state vector or density matrix")

    num_qubits = int(np.log2(vec.shape[0]))
    if vec.shape[0] != 2 ** num_qubits:
        raise ValueError("State dimension must be a power of 2")

    qargs_b = [int(q) for q in list(qargs_B)]
    if len(set(qargs_b)) != len(qargs_b):
        raise ValueError("qargs_B must contain unique qubit indices")
    if any(q < 0 or q >= num_qubits for q in qargs_b):
        raise ValueError("qargs_B contains an out-of-range qubit index")

    qargs_a = [q for q in range(num_qubits) if q not in qargs_b]

    tensor = vec.reshape([2] * num_qubits)
    transposed = np.transpose(tensor, qargs_a + qargs_b)
    dim_a = 2 ** len(qargs_a)
    dim_b = 2 ** len(qargs_b)
    matrix = transposed.reshape(dim_a, dim_b)

    u, s, vh = np.linalg.svd(matrix)

    terms = []
    for i in range(len(s)):
        terms.append((float(s[i]), u[:, i].copy(), vh[i].copy()))

    return terms
