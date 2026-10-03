# EVAL_META: task_id=139, framework=qiskit, class=2
import numpy as np
from qiskit.quantum_info import DensityMatrix, Statevector, partial_trace


def schmidt_test(data, qargs_B):
    dm = DensityMatrix(data)
    dim = dm.dim
    n = int(round(np.log2(dim)))
    if 2**n != dim:
        raise ValueError("Input density matrix dimension must be a power of 2.")

    qargs_B = list(qargs_B)
    if any((q < 0 or q >= n) for q in qargs_B):
        raise ValueError("qargs_B contains invalid qubit indices.")
    if len(set(qargs_B)) != len(qargs_B):
        raise ValueError("qargs_B contains duplicate qubit indices.")

    qargs_A = [q for q in range(n) if q not in qargs_B]
    if len(qargs_A) == 0 or len(qargs_B) == 0:
        raise ValueError("Both subsystems A and B must be non-empty.")

    evals, evecs = np.linalg.eigh(dm.data)
    idx = int(np.argmax(evals.real))
    if not np.isclose(evals[idx].real, 1.0, atol=1e-8):
        raise ValueError("Density matrix is not a pure state; Schmidt decomposition requires purity.")
    psi = evecs[:, idx]
    psi = psi / np.linalg.norm(psi)

    tensor = psi.reshape([2] * n)
    perm = qargs_A + qargs_B
    tensor_perm = np.transpose(tensor, axes=perm)
    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    mat = tensor_perm.reshape(dim_A, dim_B)

    U, S, Vh = np.linalg.svd(mat, full_matrices=False)
    terms = []
    tol = 1e-12
    for i, s in enumerate(S):
        if s > tol:
            vec_A = U[:, i]
            vec_B = np.conjugate(Vh[i, :])
            terms.append((float(np.real_if_close(s)), Statevector(vec_A), Statevector(vec_B)))
    return terms
