# EVAL_META: task_id=139, framework=qiskit, class=2
import numpy as np
from qiskit.quantum_info import DensityMatrix, partial_trace

def schmidt_test(data, qargs_B):
    rho = DensityMatrix(data)
    n = rho.num_qubits
    qargs_B = list(qargs_B)
    qargs_B_set = set(qargs_B)
    qargs_A = [i for i in range(n) if i not in qargs_B_set]

    if len(qargs_A) == 0 or len(qargs_B) == 0:
        return []

    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)

    evals, evecs = np.linalg.eigh(rho.data)
    idx = int(np.argmax(np.real(evals)))
    psi = evecs[:, idx]
    psi = psi / np.linalg.norm(psi)

    tensor_shape = (2,) * n
    psi_tensor = psi.reshape(tensor_shape)

    perm = qargs_A + qargs_B
    psi_perm = np.transpose(psi_tensor, axes=perm)
    psi_mat = psi_perm.reshape(dim_A, dim_B)

    U, S, Vh = np.linalg.svd(psi_mat, full_matrices=False)

    terms = []
    tol = 1e-12
    for i, s in enumerate(S):
        if s > tol:
            a_vec = U[:, i]
            b_vec = np.conjugate(Vh[i, :])
            terms.append((float(np.real_if_close(s)), a_vec, b_vec))

    return terms
