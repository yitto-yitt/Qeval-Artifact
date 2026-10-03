# EVAL_META: task_id=108, framework=qpanda, class=3
import numpy as np


def _to_choi(data):
    arr = np.asarray(data, dtype=complex)
    if arr.ndim == 2:
        n = arr.shape[0]
        m = arr.shape[1]
        if n == m:
            d = int(round(np.sqrt(n)))
            if d * d == n:
                return arr.copy()
        d_out = int(round(np.sqrt(arr.shape[0])))
        d_in = int(round(np.sqrt(arr.shape[1])))
        if d_out * d_out == arr.shape[0] and d_in * d_in == arr.shape[1]:
            return _superop_to_choi(arr, d_in, d_out)
        d = int(round(np.sqrt(arr.shape[0])))
        if arr.shape[0] == arr.shape[1] and d * d != arr.shape[0]:
            return _unitary_to_choi(arr)
        return _unitary_to_choi(arr)
    raise ValueError("Unsupported data format")


def _unitary_to_choi(u):
    u = np.asarray(u, dtype=complex)
    d = u.shape[0]
    vec = u.reshape(d * d, order='F')
    choi = np.zeros((d * d, d * d), dtype=complex)
    for i in range(d):
        for j in range(d):
            ei = np.zeros(d, dtype=complex)
            ei[i] = 1
            ej = np.zeros(d, dtype=complex)
            ej[j] = 1
            eij = np.outer(ei, ej)
            mapped = u @ eij @ u.conj().T
            choi += np.kron(eij, mapped)
    return choi


def _superop_to_choi(s, d_in, d_out):
    choi = np.zeros((d_in * d_out, d_in * d_out), dtype=complex)
    for i in range(d_in):
        for j in range(d_in):
            ei = np.zeros(d_in, dtype=complex)
            ei[i] = 1
            ej = np.zeros(d_in, dtype=complex)
            ej[j] = 1
            eij = np.outer(ei, ej)
            mapped_vec = s @ eij.reshape(d_in * d_in, order='F')
            mapped = mapped_vec.reshape(d_out, d_out, order='F')
            choi += np.kron(eij, mapped)
    return choi


def _choi_adjoint(choi):
    d = int(round(np.sqrt(choi.shape[0])))
    choi_r = choi.reshape(d, d, d, d)
    adj = np.conjugate(np.transpose(choi_r, (1, 0, 3, 2)))
    return adj.reshape(d * d, d * d)


def _choi_to_superop(choi, d):
    s = np.zeros((d * d, d * d), dtype=complex)
    choi_r = choi.reshape(d, d, d, d)
    for a in range(d):
        for b in range(d):
            for c in range(d):
                for e in range(d):
                    row = a * d + b
                    col = c * d + e
                    s[row, col] = choi_r[c, a, e, b]
    return s


def _superop_to_choi_sq(s, d):
    choi = np.zeros((d * d, d * d), dtype=complex)
    for i in range(d):
        for j in range(d):
            eij = np.zeros((d, d), dtype=complex)
            eij[i, j] = 1
            mapped_vec = s @ eij.reshape(d * d, order='F')
            mapped = mapped_vec.reshape(d, d, order='F')
            choi += np.kron(eij, mapped)
    return choi


def _choi_compose(choi1, choi2):
    d = int(round(np.sqrt(choi1.shape[0])))
    s1 = _choi_to_superop(choi1, d)
    s2 = _choi_to_superop(choi2, d)
    s_comp = s2 @ s1
    return _superop_to_choi_sq(s_comp, d)


def initialize_adjoint_and_compose(data1, data2):
    choi1 = _to_choi(data1)
    choi2 = _to_choi(data2)
    adjoint_choi1 = _choi_adjoint(choi1)
    composed_choi = _choi_compose(choi1, choi2)
    return choi1, adjoint_choi1, composed_choi
