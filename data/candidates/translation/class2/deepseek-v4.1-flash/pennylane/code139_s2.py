# EVAL_META: task_id=139, framework=pennylane, class=2
import numpy as np
import pennylane as qml


def schmidt_test(data, qargs_B):
    if not isinstance(data, np.ndarray):
        try:
            data = np.asarray(data, dtype=complex)
        except Exception:
            data = np.asarray(data.data, dtype=complex)
    else:
        data = data.astype(complex)

    dim = data.shape[0]
    n = int(round(np.log2(dim)))
    qargs_B = [int(q) for q in qargs_B]
    qargs_A = [i for i in range(n) if i not in qargs_B]

    order = qargs_A + qargs_B
    dA = 2 ** len(qargs_A)
    dB = 2 ** len(qargs_B)

    if data.ndim == 1:
        psi_tensor = data.reshape([2] * n)
        perm_psi = [n - 1 - q for q in order]
        psi_reordered = np.transpose(psi_tensor, perm_psi).reshape(dA, dB)
        u, s, vh = np.linalg.svd(psi_reordered, full_matrices=False)
        terms = []
        for k in range(len(s)):
            if s[k] < 1e-12:
                break
            terms.append((complex(s[k]), u[:, k].astype(complex), vh[k, :].astype(complex)))
        return terms

    rho = data
    rho_tensor = rho.reshape([2] * (2 * n))
    perm = [n - 1 - q for q in order] + [2 * n - 1 - q for q in order]
    rho_reordered = np.transpose(rho_tensor, perm).reshape(dim, dim)
    rho_ab = rho_reordered.reshape(dA, dB, dA, dB)
    rho_A = np.trace(rho_ab, axis1=1, axis2=3)

    eigvals, eigvecs = np.linalg.eigh(rho_A)
    idx = np.argsort(-eigvals)
    eigvals = eigvals[idx]
    eigvecs = eigvecs[:, idx]

    terms = []
    for k in range(len(eigvals)):
        lam = eigvals[k]
        if lam < 1e-12:
            break
        a_vec = eigvecs[:, k]
        T = np.einsum('a,abac,c->bc', a_vec.conj(), rho_ab, a_vec)
        col_norms = np.linalg.norm(T, axis=0)
        j = int(np.argmax(col_norms))
        b_vec = T[:, j]
        nrm = np.linalg.norm(b_vec)
        if nrm > 1e-12:
            b_vec = b_vec / nrm
        terms.append((complex(np.sqrt(lam)), a_vec.astype(complex), b_vec.astype(complex)))
    return terms
