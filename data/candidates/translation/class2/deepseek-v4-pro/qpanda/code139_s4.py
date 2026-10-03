# EVAL_META: task_id=139, framework=qpanda, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    arr = np.asarray(data, dtype=complex)

    if arr.ndim == 1:
        psi = arr
    elif arr.ndim == 2 and arr.shape[0] == arr.shape[1]:
        rho = arr
        eigvals_rho, eigvecs_rho = np.linalg.eigh(rho)
        if not np.isclose(eigvals_rho[-1], 1.0, atol=1e-10) or np.any(np.abs(eigvals_rho[:-1]) > 1e-10):
            raise ValueError("Input density matrix is not pure")
        psi = eigvecs_rho[:, -1]
    else:
        raise ValueError("Input must be a 1D statevector or a square density matrix")

    norm = np.linalg.norm(psi)
    if norm == 0:
        raise ValueError("Zero state vector")
    psi = psi / norm

    n_qubits = int(round(np.log2(psi.shape[0])))
    if 2 ** n_qubits != psi.shape[0]:
        raise ValueError("Statevector length must be a power of 2")

    if isinstance(qargs_B, int):
        qargs_B = [qargs_B]
    qargs_B = list(qargs_B)
    if len(qargs_B) == 0 or len(qargs_B) == n_qubits:
        raise ValueError("qargs_B must be a proper subset of qubits")
    if len(set(qargs_B)) != len(qargs_B):
        raise ValueError("Duplicate qubit indices in qargs_B")
    if not all(0 <= q < n_qubits for q in qargs_B):
        raise ValueError("Invalid qubit index in qargs_B")

    qargs_A = [i for i in range(n_qubits) if i not in qargs_B]
    dims_a = 2 ** len(qargs_A)
    dims_b = 2 ** len(qargs_B)

    mat = np.zeros((dims_a, dims_b), dtype=complex)
    for full_idx, coeff in enumerate(psi):
        a_idx = 0
        for j, q in enumerate(qargs_A):
            if (full_idx >> q) & 1:
                a_idx |= (1 << j)

        b_idx = 0
        for j, q in enumerate(qargs_B):
            if (full_idx >> q) & 1:
                b_idx |= (1 << j)

        mat[a_idx, b_idx] = coeff

    rho_a = mat @ mat.conj().T
    eigvals, eigvecs = np.linalg.eigh(rho_a)

    eigvals = eigvals[::-1]
    eigvecs = eigvecs[:, ::-1]

    terms = []
    tol = 1e-12
    for i, val in enumerate(eigvals):
        if val > tol:
            coeff = float(np.sqrt(val))
            state_a = eigvecs[:, i].copy()
            state_b = mat.T @ state_a.conj() / coeff
            state_b /= np.linalg.norm(state_b)
            terms.append((coeff, state_a, state_b))

    return terms
