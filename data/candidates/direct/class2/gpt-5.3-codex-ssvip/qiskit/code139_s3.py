# EVAL_META: task_id=139, framework=qiskit, class=2
import numpy as np
from qiskit.quantum_info import DensityMatrix, Statevector


def schmidt_test(data, qargs_B):
    dm = DensityMatrix(data)
    n = dm.num_qubits
    qargs_B = list(qargs_B)
    qargs_B_set = set(qargs_B)
    qargs_A = [i for i in range(n) if i not in qargs_B_set]

    rho = np.asarray(dm.data, dtype=complex)
    evals, evecs = np.linalg.eigh(rho)
    idx = int(np.argmax(np.real(evals)))
    psi = evecs[:, idx]
    norm = np.linalg.norm(psi)
    if norm > 0:
        psi = psi / norm

    dims = [2] * n
    tensor = psi.reshape(dims)

    perm = qargs_A + qargs_B
    if len(perm) != n or sorted(perm) != list(range(n)):
        raise ValueError("Invalid partition qargs_B for the number of qubits.")

    tensor_perm = np.transpose(tensor, axes=perm)
    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    mat = tensor_perm.reshape(dim_A, dim_B)

    U, S, Vh = np.linalg.svd(mat, full_matrices=False)

    terms = []
    tol = 1e-12
    for i, s in enumerate(S):
        if float(np.real_if_close(s)) > tol:
            vec_A = U[:, i]
            vec_B = np.conjugate(Vh[i, :])
            terms.append((float(np.real_if_close(s)), Statevector(vec_A), Statevector(vec_B)))

    return terms
