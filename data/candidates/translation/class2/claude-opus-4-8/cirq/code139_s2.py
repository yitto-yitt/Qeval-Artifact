# EVAL_META: task_id=139, framework=cirq, class=2
import numpy as np


def _to_statevector(data, num_qubits):
    arr = np.asarray(data, dtype=complex)
    if arr.ndim == 1:
        return arr
    if arr.ndim == 2 and arr.shape[0] == arr.shape[1]:
        vals, vecs = np.linalg.eigh(arr)
        idx = int(np.argmax(vals.real))
        vec = vecs[:, idx]
        vec = vec * np.sqrt(max(vals[idx].real, 0.0))
        return vec
    return arr.reshape(-1)


def schmidt_test(data, qargs_B):
    total = np.asarray(data, dtype=complex)
    if total.ndim == 2 and total.shape[0] == total.shape[1]:
        dim = total.shape[0]
    else:
        dim = np.asarray(total).reshape(-1).shape[0]
    num_qubits = int(round(np.log2(dim)))

    state = _to_statevector(data, num_qubits)
    state = state.reshape([2] * num_qubits)

    qargs_B = list(qargs_B)
    qargs_A = [q for q in range(num_qubits) if q not in qargs_B]

    perm = qargs_A + qargs_B
    permuted = np.transpose(state, perm)

    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    mat = permuted.reshape(dim_A, dim_B)

    u, s, vh = np.linalg.svd(mat, full_matrices=False)

    terms = []
    for i in range(len(s)):
        coeff = s[i]
        if coeff <= 1e-12:
            continue
        vec_A = u[:, i]
        vec_B = vh[i, :]
        terms.append((float(coeff), vec_A, vec_B))

    return terms
