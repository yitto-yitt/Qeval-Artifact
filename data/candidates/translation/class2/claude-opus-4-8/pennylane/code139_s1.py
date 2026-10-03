# EVAL_META: task_id=139, framework=pennylane, class=2
import numpy as np


def schmidt_test(data, qargs_B):
    if hasattr(data, "data"):
        state = np.asarray(data.data, dtype=complex)
    else:
        state = np.asarray(data, dtype=complex)

    if state.ndim == 2 and state.shape[0] == state.shape[1] and state.shape[0] > 1:
        vals, vecs = np.linalg.eigh(state)
        idx = int(np.argmax(vals.real))
        state = vecs[:, idx]

    state = np.asarray(state).reshape(-1)
    dim = state.shape[0]
    num_qubits = int(round(np.log2(dim)))

    qargs_B = list(qargs_B)
    all_qubits = list(range(num_qubits))
    qargs_A = [q for q in all_qubits if q not in qargs_B]

    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)

    tensor = state.reshape([2] * num_qubits)

    A_axes = [num_qubits - 1 - q for q in qargs_A]
    B_axes = [num_qubits - 1 - q for q in qargs_B]

    perm = A_axes + B_axes
    mat = np.transpose(tensor, perm).reshape(dim_A, dim_B)

    U, S, Vh = np.linalg.svd(mat)

    terms = []
    for i in range(len(S)):
        coeff = S[i]
        if coeff <= 1e-12:
            continue
        vec_A = U[:, i]
        vec_B = Vh[i, :]
        terms.append((coeff, vec_A, vec_B))

    return terms
