# EVAL_META: task_id=108, framework=pennylane, class=3
import numpy as np


def _vectorize_col(matrix):
    return np.asarray(matrix).reshape(-1, order="F")


def _kraus_to_choi(kraus, dim=None):
    if not kraus:
        if dim is None:
            raise ValueError("Cannot infer dimension from an empty Kraus list")
        return np.zeros((dim, dim), dtype=complex)

    d_out, d_in = kraus[0].shape
    dim = d_out * d_in
    choi = np.zeros((dim, dim), dtype=complex)
    for k in kraus:
        v = _vectorize_col(k)
        choi += np.outer(v, v.conj())
    return choi


def _choi_to_kraus(choi, d_out, d_in):
    eigvals, eigvecs = np.linalg.eigh(choi)
    kraus = []
    tol = 1e-12
    for val, vec in zip(eigvals, eigvecs.T):
        if val > tol:
            kraus.append(np.sqrt(val) * vec.reshape((d_out, d_in), order="F"))
    return kraus


def _infer_dim(choi):
    if choi.ndim != 2 or choi.shape[0] != choi.shape[1]:
        raise ValueError("Choi matrix must be square")
    dim = choi.shape[0]
    d = int(np.sqrt(dim))
    if d * d != dim:
        raise ValueError("Cannot infer input and output dimensions from Choi matrix")
    return d


def initialize_adjoint_and_compose(data1, data2):
    choi1 = np.asarray(data1, dtype=complex)
    choi2 = np.asarray(data2, dtype=complex)

    d1 = _infer_dim(choi1)
    d2 = _infer_dim(choi2)

    if d1 != d2:
        raise ValueError("Cannot compose channels with different dimensions")

    kraus1 = _choi_to_kraus(choi1, d1, d1)
    kraus2 = _choi_to_kraus(choi2, d2, d2)

    adjoint_kraus1 = [k.conj().T for k in kraus1]
    adjoint_choi1 = _kraus_to_choi(adjoint_kraus1, dim=choi1.shape[0])

    composed_kraus = [a @ b for a in kraus1 for b in kraus2]
    composed_choi = _kraus_to_choi(composed_kraus, dim=choi1.shape[0])

    return choi1, adjoint_choi1, composed_choi
