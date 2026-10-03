# EVAL_META: task_id=108, framework=qpanda, class=3
import numpy as np


def _to_choi(data):
    arr = np.array(data, dtype=complex)
    if arr.ndim == 2 and arr.shape[0] == arr.shape[1]:
        d = arr.shape[0]
        root = int(round(np.sqrt(d)))
        if root * root == d:
            # Could be either a unitary (dim = root) or already a Choi (dim = d)
            # Heuristic: treat square matrix whose size is a perfect square and
            # that is not unitary as a Choi matrix; otherwise treat as unitary.
            u = arr
            if np.allclose(u.conj().T @ u, np.eye(d)):
                return _unitary_to_choi(u)
            return arr
        else:
            # square but dim not a perfect square -> unitary operator
            return _unitary_to_choi(arr)
    else:
        raise ValueError("Unsupported input data for Choi construction")


def _unitary_to_choi(u):
    d = u.shape[0]
    choi = np.zeros((d * d, d * d), dtype=complex)
    for i in range(d):
        for j in range(d):
            e_ij = np.zeros((d, d), dtype=complex)
            e_ij[i, j] = 1.0
            mapped = u @ e_ij @ u.conj().T
            choi += np.kron(e_ij, mapped)
    return choi


def _choi_to_kraus(choi, dim_in, dim_out):
    vals, vecs = np.linalg.eigh(choi)
    kraus = []
    for k in range(len(vals)):
        v = vals[k]
        if abs(v) < 1e-12:
            continue
        vec = vecs[:, k] * np.sqrt(complex(v))
        # reshape column-stacking (Choi convention: |i>|j> ordering row-major on input)
        K = vec.reshape(dim_in, dim_out).T
        kraus.append(K)
    return kraus


def _kraus_to_choi(kraus, dim_in, dim_out):
    choi = np.zeros((dim_in * dim_out, dim_in * dim_out), dtype=complex)
    for i in range(dim_in):
        for j in range(dim_in):
            e_ij = np.zeros((dim_in, dim_in), dtype=complex)
            e_ij[i, j] = 1.0
            acc = np.zeros((dim_out, dim_out), dtype=complex)
            for K in kraus:
                acc += K @ e_ij @ K.conj().T
            choi += np.kron(e_ij, acc)
    return choi


def _choi_adjoint(choi):
    d2 = choi.shape[0]
    d = int(round(np.sqrt(d2)))
    kraus = _choi_to_kraus(choi, d, d)
    adj_kraus = [K.conj().T for K in kraus]
    return _kraus_to_choi(adj_kraus, d, d)


def _choi_compose(choi1, choi2):
    d = int(round(np.sqrt(choi1.shape[0])))
    kraus1 = _choi_to_kraus(choi1, d, d)
    kraus2 = _choi_to_kraus(choi2, d, d)
    composed = []
    for B in kraus2:
        for A in kraus1:
            composed.append(B @ A)
    return _kraus_to_choi(composed, d, d)


def initialize_adjoint_and_compose(data1, data2):
    choi1 = _to_choi(data1)
    choi2 = _to_choi(data2)
    adjoint_choi1 = _choi_adjoint(choi1)
    composed_choi = _choi_compose(choi1, choi2)
    return choi1, adjoint_choi1, composed_choi
