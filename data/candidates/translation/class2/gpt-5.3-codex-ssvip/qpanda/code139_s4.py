# EVAL_META: task_id=139, framework=qpanda, class=2
import numpy as np
from pyqpanda3.core import *

def schmidt_test(data, qargs_B):
    arr = np.asarray(data, dtype=complex)
    if arr.ndim == 1:
        n = int(round(np.log2(arr.size)))
        if 2 ** n != arr.size:
            raise ValueError("Statevector length must be a power of 2.")
        psi = arr.reshape([2] * n)
        qargs_B = list(qargs_B)
        qargs_A = [i for i in range(n) if i not in qargs_B]
        perm = qargs_A + qargs_B
        psi_perm = np.transpose(psi, axes=perm)
        dim_A = 2 ** len(qargs_A)
        dim_B = 2 ** len(qargs_B)
        mat = psi_perm.reshape(dim_A, dim_B)
        U, s, Vh = np.linalg.svd(mat, full_matrices=False)
        terms = []
        for i, coeff in enumerate(s):
            if abs(coeff) > 1e-12:
                a_vec = U[:, i]
                b_vec = np.conjugate(Vh[i, :])
                terms.append((coeff, a_vec, b_vec))
        return terms

    if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
        raise ValueError("Input must be a statevector or square density matrix.")
    dim = arr.shape[0]
    n = int(round(np.log2(dim)))
    if 2 ** n != dim:
        raise ValueError("Density matrix dimension must be a power of 2.")

    evals, evecs = np.linalg.eigh(arr)
    idx = np.argmax(evals.real)
    psi = evecs[:, idx]
    psi = psi / np.linalg.norm(psi)

    psi_t = psi.reshape([2] * n)
    qargs_B = list(qargs_B)
    qargs_A = [i for i in range(n) if i not in qargs_B]
    perm = qargs_A + qargs_B
    psi_perm = np.transpose(psi_t, axes=perm)
    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    mat = psi_perm.reshape(dim_A, dim_B)

    U, s, Vh = np.linalg.svd(mat, full_matrices=False)
    terms = []
    for i, coeff in enumerate(s):
        if abs(coeff) > 1e-12:
            a_vec = U[:, i]
            b_vec = np.conjugate(Vh[i, :])
            terms.append((coeff, a_vec, b_vec))
    return terms
