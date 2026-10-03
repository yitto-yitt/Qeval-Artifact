# EVAL_META: task_id=139, framework=qiskit, class=2
import numpy as np
from qiskit.quantum_info import DensityMatrix, partial_trace, Statevector

def schmidt_test(data, qargs_B):
    dm = DensityMatrix(data)
    n = dm.num_qubits
    qargs_B = list(qargs_B)
    qargs_B_set = set(qargs_B)
    qargs_A = [i for i in range(n) if i not in qargs_B_set]

    rho = np.asarray(dm.data, dtype=complex)

    dims = [2] * n
    tensor = rho.reshape(dims + dims)

    perm = qargs_A + qargs_B + [i + n for i in qargs_A] + [i + n for i in qargs_B]
    tensor_perm = np.transpose(tensor, perm)

    dimA = 2 ** len(qargs_A)
    dimB = 2 ** len(qargs_B)
    rho_ab = tensor_perm.reshape(dimA * dimB, dimA * dimB)

    evals, evecs = np.linalg.eigh(rho_ab)
    idx = np.argmax(evals.real)
    psi = evecs[:, idx]
    if np.abs(psi[0]) > 1e-15:
        psi = psi * np.exp(-1j * np.angle(psi[0]))

    M = psi.reshape(dimA, dimB)
    U, s, Vh = np.linalg.svd(M, full_matrices=False)

    terms = []
    tol = 1e-12
    for i, coeff in enumerate(s):
        c = float(np.real_if_close(coeff))
        if c > tol:
            vecA = U[:, i]
            vecB = np.conjugate(Vh[i, :])
            terms.append((c, Statevector(vecA), Statevector(vecB)))
    return terms
