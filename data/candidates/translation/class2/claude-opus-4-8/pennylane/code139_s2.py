# EVAL_META: task_id=139, framework=pennylane, class=2
import numpy as np
import pennylane as qml


def schmidt_test(data, qargs_B):
    if hasattr(data, "data"):
        state = np.asarray(data.data)
    else:
        state = np.asarray(data)

    if state.ndim == 2:
        if state.shape[0] == state.shape[1] and not np.allclose(
            state, np.outer(state[:, 0], np.conj(state[:, 0]))
        ):
            evals, evecs = np.linalg.eigh(state)
            idx = int(np.argmax(evals))
            vec = evecs[:, idx]
        else:
            vec = state.reshape(-1)
    else:
        vec = state.reshape(-1)

    dim = vec.shape[0]
    num_qubits = int(round(np.log2(dim)))

    qargs_B = list(qargs_B)
    qargs_A = [q for q in range(num_qubits) if q not in qargs_B]

    tensor = vec.reshape([2] * num_qubits)

    perm = qargs_A + qargs_B
    tensor = np.transpose(tensor, perm)

    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    mat = tensor.reshape(dim_A, dim_B)

    U, S, Vh = np.linalg.svd(mat)

    terms = []
    for i in range(len(S)):
        coeff = S[i]
        if coeff <= 1e-12:
            continue
        a_vec = U[:, i]
        b_vec = Vh[i, :]
        terms.append((coeff, a_vec, b_vec))

    return terms
