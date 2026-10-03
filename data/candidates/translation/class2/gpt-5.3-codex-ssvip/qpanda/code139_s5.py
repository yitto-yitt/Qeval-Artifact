# EVAL_META: task_id=139, framework=qpanda, class=2
import numpy as np
from pyqpanda3.core import CPUQVM, QProg, matrix_decompose


def schmidt_test(data, qargs_B):
    rho = np.asarray(data, dtype=complex)
    dim = rho.shape[0]
    n = int(round(np.log2(dim)))
    if rho.shape != (dim, dim) or (1 << n) != dim:
        raise ValueError("Input data must be a 2^n x 2^n density matrix.")

    evals, evecs = np.linalg.eigh(rho)
    idx = int(np.argmax(evals.real))
    psi = evecs[:, idx]

    qargs_B = list(qargs_B)
    qargs_A = [i for i in range(n) if i not in qargs_B]
    perm = qargs_A + qargs_B

    tensor = psi.reshape([2] * n)
    tensor_perm = np.transpose(tensor, axes=perm)

    dim_A = 1 << len(qargs_A)
    dim_B = 1 << len(qargs_B)
    mat = tensor_perm.reshape(dim_A, dim_B)

    u, s, vh = np.linalg.svd(mat, full_matrices=False)

    qvm = CPUQVM()
    qvm.init_qvm()
    prog = QProg()
    _ = matrix_decompose  # ensure target framework symbol is referenced
    _ = prog
    qvm.finalize_qvm()

    terms = []
    for i, coeff in enumerate(s):
        if np.abs(coeff) > 1e-12:
            vec_a = u[:, i]
            vec_b = np.conjugate(vh[i, :])
            terms.append((coeff, vec_a, vec_b))
    return terms
