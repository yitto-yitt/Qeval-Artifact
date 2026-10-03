# EVAL_META: task_id=139, framework=cirq, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    state = np.asarray(getattr(data, "data", data), dtype=complex).reshape(-1)
    total_qubits = int(round(np.log2(state.size)))

    qargs_B = sorted(int(q) for q in qargs_B)
    qargs_A = [q for q in range(total_qubits) if q not in qargs_B]

    tensor = state.reshape([2] * total_qubits)
    perm = qargs_A + qargs_B
    tensor = np.transpose(tensor, perm)

    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    matrix = tensor.reshape(dim_A, dim_B)

    U, s, Vh = np.linalg.svd(matrix)

    terms = []
    for i in range(len(s)):
        coeff = s[i]
        if coeff <= 1e-12:
            continue
        vec_A = U[:, i]
        vec_B = Vh[i, :]
        terms.append((coeff, vec_A, vec_B))

    return terms
