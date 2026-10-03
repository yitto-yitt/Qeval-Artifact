# EVAL_META: task_id=139, framework=cirq, class=2
import numpy as np

def _schmidt_pure(psi, qargs_B, num_qubits):
    """Compute Schmidt decomposition of a pure state vector in little‑endian basis."""
    # psi is 1D array of length 2**num_qubits
    tensor = psi.reshape([2] * num_qubits)  # axis 0 -> qubit (num_qubits-1), ... axis (num_qubits-1) -> qubit 0
    # reverse axes so that axis q corresponds to qubit q
    tensor = tensor.transpose(list(range(num_qubits - 1, -1, -1)))
    A_qubits = [i for i in range(num_qubits) if i not in qargs_B]
    order = A_qubits + list(qargs_B)
    tensor = tensor.transpose(order)
    mat = tensor.reshape((2 ** len(A_qubits), 2 ** len(qargs_B)))
    U, s, Vh = np.linalg.svd(mat, full_matrices=False)
    terms = []
    for k in range(len(s)):
        coeff = float(s[k])
        state_A = U[:, k].copy()
        state_B = Vh[k].conj().copy()  # V[:,k] = conj(Vh[k])
        terms.append((coeff, state_A, state_B))
    return terms

def schmidt_test(data, qargs_B):
    data = np.asarray(data, dtype=complex)
    if data.ndim == 1:
        n = int(np.log2(len(data)))
        return _schmidt_pure(data, qargs_B, n)
    # density matrix
    n = int(np.log2(data.shape[0]))
    purity = np.trace(data @ data).real
    if np.abs(purity - 1.0) < 1e-10:
        # pure density matrix: use its eigenstate
        eigenvalues, eigenvectors = np.linalg.eigh(data)
        idx = np.argmax(eigenvalues)  # eigenvalue ~ 1
        psi = eigenvectors[:, idx]
        psi /= np.linalg.norm(psi)
        return _schmidt_pure(psi, qargs_B, n)
    # mixed state: purify via spectral decomposition
    eigenvalues, eigenvectors = np.linalg.eigh(data)
    # sort descending
    idx_sort = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[idx_sort]
    eigenvectors = eigenvectors[:, idx_sort]
    dim = 2 ** n
    psi_combined = np.zeros(dim * dim, dtype=complex)
    for k in range(len(eigenvalues)):
        w = eigenvalues[k]
        if w <= 0:
            continue
        v = eigenvectors[:, k]
        # build in little‑endian order: idx = i_orig + (i_anc << n)
        for i_orig in range(dim):
            for i_anc in range(dim):
                idx = i_orig + (i_anc << n)
                psi_combined[idx] += np.sqrt(w) * v[i_orig] * v[i_anc]
    return _schmidt_pure(psi_combined, qargs_B, 2 * n)
