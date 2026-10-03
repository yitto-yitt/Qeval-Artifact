# EVAL_META: task_id=139, framework=pennylane, class=2
import numpy as np
import pennylane as qml


def schmidt_test(data, qargs_B):
    state = np.asarray(getattr(data, "data", data), dtype=complex)

    if state.ndim == 2:
        n = int(round(np.log2(state.shape[0])))
        rank = np.linalg.matrix_rank(state)
        if state.shape[0] == state.shape[1] and rank > 1:
            evals, evecs = np.linalg.eigh(state)
            idx = int(np.argmax(evals.real))
            vec = evecs[:, idx]
            vec = vec / np.linalg.norm(vec)
        else:
            vec = state.reshape(-1)
            vec = vec / np.linalg.norm(vec)
    else:
        vec = state / np.linalg.norm(state)
        n = int(round(np.log2(vec.shape[0])))

    all_qubits = list(range(n))
    qargs_B = list(qargs_B)
    qargs_A = [q for q in all_qubits if q not in qargs_B]

    dimsA = 2 ** len(qargs_A)
    dimsB = 2 ** len(qargs_B)

    tensor = vec.reshape([2] * n)

    perm = qargs_A + qargs_B
    tensor = np.transpose(tensor, perm)
    mat = tensor.reshape(dimsA, dimsB)

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
