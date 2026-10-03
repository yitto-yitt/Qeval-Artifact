# EVAL_META: task_id=139, framework=cirq, class=2
import numpy as np


def schmidt_test(data, qargs_B):
    state = np.asarray(getattr(data, "data", data), dtype=complex).reshape(-1)
    total_qubits = int(round(np.log2(state.shape[0])))

    qargs_B = sorted(int(q) for q in qargs_B)
    qargs_A = [q for q in range(total_qubits) if q not in qargs_B]

    def bit_index(qubit):
        return total_qubits - 1 - qubit

    tensor = state.reshape([2] * total_qubits)

    a_axes = [bit_index(q) for q in reversed(qargs_A)]
    b_axes = [bit_index(q) for q in reversed(qargs_B)]

    permuted = np.transpose(tensor, a_axes + b_axes)
    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    matrix = permuted.reshape(dim_A, dim_B)

    U, S, Vh = np.linalg.svd(matrix, full_matrices=False)

    terms = []
    for i in range(len(S)):
        coeff = S[i]
        if coeff <= 1e-12:
            continue
        vec_A = U[:, i]
        vec_B = Vh[i, :]
        terms.append((float(coeff), vec_A, vec_B))

    return terms
