# EVAL_META: task_id=139, framework=cirq, class=2
import numpy as np


def schmidt_test(data, qargs_B):
    data = np.asarray(data)

    if data.ndim == 1:
        psi = data
    elif data.ndim == 2:
        rho = data
        # Extract pure-state eigenvector from the density matrix.
        eigvals, eigvecs = np.linalg.eigh(rho)
        idx = int(np.argmax(eigvals))
        psi = eigvecs[:, idx]
        if not np.isclose(np.max(eigvals), 1.0, atol=1e-8):
            raise ValueError("Input density matrix is not pure")
    else:
        raise ValueError("Input must be a state vector or density matrix")

    n = int(np.round(np.log2(psi.shape[0])))
    if 2**n != psi.shape[0]:
        raise ValueError("State dimension must be a power of 2")

    qargs_B = list(qargs_B)
    all_indices = set(range(n))
    B_set = set(qargs_B)
    if not B_set.issubset(all_indices) or len(B_set) != len(qargs_B):
        raise ValueError("Invalid qargs_B")
    if len(qargs_B) == n:
        raise ValueError("qargs_B must be a proper subset of the qubits")

    A = sorted(all_indices - B_set)
    new_order = A + qargs_B

    psi_tensor = psi.reshape((2,) * n)
    psi_perm = np.transpose(psi_tensor, new_order)

    dimA = 2 ** len(A)
    dimB = 2 ** len(qargs_B)
    mat = psi_perm.reshape((dimA, dimB))

    u, s, vh = np.linalg.svd(mat, full_matrices=False)

    terms = []
    for i in range(len(s)):
        coeff = float(s[i])
        state_a = u[:, i]
        state_b = vh[i, :]
        terms.append((coeff, state_a, state_b))

    return terms
