# EVAL_META: task_id=139, framework=pennylane, class=2
import numpy as np
import pennylane as qml


def schmidt_test(data, qargs_B):
    data = np.asarray(data, dtype=complex)

    if data.ndim == 2:
        vals, vecs = np.linalg.eigh(data)
        idx = int(np.argmax(vals.real))
        state = vecs[:, idx]
    else:
        state = data.reshape(-1)

    dim = state.shape[0]
    num_qubits = int(round(np.log2(dim)))

    all_qubits = list(range(num_qubits))
    qargs_B = list(qargs_B)
    qargs_A = [q for q in all_qubits if q not in qargs_B]

    tensor = state.reshape([2] * num_qubits)

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
        vec_A = U[:, i]
        vec_B = Vh[i, :].conj()
        terms.append((coeff, vec_A, vec_B))

    return terms
