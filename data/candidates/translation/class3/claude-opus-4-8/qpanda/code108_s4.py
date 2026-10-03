# EVAL_META: task_id=108, framework=qpanda, class=3
import numpy as np


def _to_choi(data):
    arr = np.asarray(data, dtype=complex)
    if arr.ndim == 2 and arr.shape[0] == arr.shape[1]:
        n = arr.shape[0]
        r = int(round(np.log2(n)))
        if (1 << r) == n and _is_choi_like(arr):
            return arr
    return _superop_to_choi(_to_superop(arr))


def _is_choi_like(arr):
    return np.allclose(arr, arr.conj().T)


def _to_superop(data):
    arr = np.asarray(data, dtype=complex)
    d = arr.shape[0]
    dim = int(round(np.sqrt(d)))
    if dim * dim == d and arr.ndim == 2 and arr.shape[0] == arr.shape[1]:
        if _looks_unitary(arr):
            return np.kron(arr.conj(), arr)
    if arr.ndim == 2 and arr.shape[0] == arr.shape[1] and _looks_unitary(arr):
        return np.kron(arr.conj(), arr)
    return np.kron(arr.conj(), arr)


def _looks_unitary(arr):
    if arr.shape[0] != arr.shape[1]:
        return False
    ident = np.eye(arr.shape[0])
    return np.allclose(arr.conj().T @ arr, ident)


def _superop_to_choi(superop):
    d2 = superop.shape[0]
    d = int(round(np.sqrt(d2)))
    choi = np.zeros((d * d, d * d), dtype=complex)
    for i in range(d):
        for j in range(d):
            for k in range(d):
                for l in range(d):
                    row_s = i * d + j
                    col_s = k * d + l
                    row_c = j * d + l
                    col_c = i * d + k
                    choi[row_c, col_c] = superop[row_s, col_s]
    return choi


def _choi_adjoint(choi):
    d2 = choi.shape[0]
    d = int(round(np.sqrt(d2)))
    superop = _choi_to_superop(choi, d)
    adj_superop = superop.conj().T
    return _superop_to_choi(adj_superop)


def _choi_to_superop(choi, d):
    superop = np.zeros((d * d, d * d), dtype=complex)
    for i in range(d):
        for j in range(d):
            for k in range(d):
                for l in range(d):
                    row_s = i * d + j
                    col_s = k * d + l
                    row_c = j * d + l
                    col_c = i * d + k
                    superop[row_s, col_s] = choi[row_c, col_c]
    return superop


def _choi_compose(choi1, choi2):
    d = int(round(np.sqrt(choi1.shape[0])))
    s1 = _choi_to_superop(choi1, d)
    s2 = _choi_to_superop(choi2, d)
    composed = s2 @ s1
    return _superop_to_choi(composed)


def initialize_adjoint_and_compose(data1, data2):
    choi1 = _to_choi(data1)
    choi2 = _to_choi(data2)
    adjoint_choi1 = _choi_adjoint(choi1)
    composed_choi = _choi_compose(choi1, choi2)
    return choi1, adjoint_choi1, composed_choi
