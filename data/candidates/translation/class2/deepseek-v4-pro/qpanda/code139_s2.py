# EVAL_META: task_id=139, framework=qpanda, class=2
import numpy as np
import pyqpanda3.core as pq

def schmidt_test(data, qargs_B):
    data = np.asarray(data, dtype=complex)
    if data.ndim == 2:
        n = int(round(np.log2(data.shape[0])))
        rho = data
        eigvals, eigvecs = np.linalg.eigh(rho)
        ket = eigvecs[:, int(np.argmax(eigvals))]
    elif data.ndim == 1:
        n = int(round(np.log2(data.shape[0])))
        ket = data
    else:
        raise ValueError("Input must be a state vector or density matrix")

    ket = ket / np.linalg.norm(ket)

    if qargs_B is None:
        qargs_B = list(range(n))
    elif isinstance(qargs_B, (int, np.integer)):
        qargs_B = [int(qargs_B)]
    else:
        qargs_B = [int(q) for q in qargs_B]

    if any(q < 0 or q >= n for q in qargs_B):
        raise ValueError("qargs_B contains an invalid qubit index")
    if len(set(qargs_B)) != len(qargs_B):
        raise ValueError("qargs_B contains duplicate qubit indices")

    qargs_B = sorted(qargs_B)
    qargs_A = [q for q in range(n) if q not in set(qargs_B)]

    psi_tensor = ket.reshape([2] * n)
    perm = qargs_A + qargs_B
    psi_tensor = np.transpose(psi_tensor, perm)

    dim_a = 2 ** len(qargs_A)
    dim_b = 2 ** len(qargs_B)
    psi_matrix = psi_tensor.reshape((dim_a, dim_b))

    u, s, vh = np.linalg.svd(psi_matrix, full_matrices=False)

    terms = []
    for i in range(len(s)):
        if s[i] < 1e-12:
            continue
        vec_a = u[:, i].reshape([2] * len(qargs_A)).flatten()
        vec_b = vh[i].reshape([2] * len(qargs_B)).flatten()
        terms.append((float(s[i]), vec_a, vec_b))

    return terms
