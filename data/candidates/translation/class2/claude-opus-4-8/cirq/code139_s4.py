# EVAL_META: task_id=139, framework=cirq, class=2
import numpy as np
import cirq


def schmidt_test(data, qargs_B):
    state = np.asarray(getattr(data, "data", data), dtype=complex).reshape(-1)
    norm = np.linalg.norm(state)
    if norm != 0:
        state = state / norm

    total = state.shape[0]
    num_qubits = int(round(np.log2(total)))
    if 2 ** num_qubits != total:
        raise ValueError("State dimension must be a power of 2.")

    qargs_B = sorted(int(q) for q in qargs_B)
    all_qubits = list(range(num_qubits))
    qargs_A = [q for q in all_qubits if q not in qargs_B]

    # Qiskit uses little-endian bit ordering (qubit 0 is least significant).
    # Reshape state into a tensor with axis order from most significant to least.
    tensor = state.reshape([2] * num_qubits)
    axis_order = list(range(num_qubits - 1, -1, -1))  # axis i corresponds to qubit

    def qubit_to_axis(q):
        return axis_order.index(q)

    axes_A = [qubit_to_axis(q) for q in qargs_A]
    axes_B = [qubit_to_axis(q) for q in qargs_B]

    perm = axes_A + axes_B
    tensor = np.transpose(tensor, perm)

    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    mat = tensor.reshape(dim_A, dim_B)

    u, s, vh = np.linalg.svd(mat, full_matrices=False)

    terms = []
    tol = 1e-12
    for i in range(len(s)):
        coeff = s[i]
        if coeff <= tol:
            continue
        vec_A = u[:, i]
        vec_B = vh[i, :]
        terms.append((float(coeff), vec_A, vec_B))

    return terms
