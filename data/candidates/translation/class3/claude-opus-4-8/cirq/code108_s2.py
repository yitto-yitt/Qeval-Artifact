# EVAL_META: task_id=108, framework=cirq, class=3
import numpy as np


def _to_choi(data):
    if isinstance(data, np.ndarray):
        return np.array(data, dtype=complex)
    arr = np.array(data, dtype=complex)
    if arr.ndim == 2 and arr.shape[0] == arr.shape[1]:
        d = arr.shape[0]
        s = int(round(np.sqrt(d)))
        if s * s == d:
            return arr
    return arr


def _dim_from_choi(choi):
    d = int(round(np.sqrt(choi.shape[0])))
    return d


def _adjoint_choi(choi):
    d = _dim_from_choi(choi)
    perm = np.zeros((d * d, d * d), dtype=complex)
    for i in range(d):
        for j in range(d):
            perm[j * d + i, i * d + j] = 1.0
    return perm @ choi.conj() @ perm


def _compose_choi(choi_a, choi_b):
    d = _dim_from_choi(choi_a)

    def choi_to_superop(choi):
        s = np.zeros((d * d, d * d), dtype=complex)
        for i in range(d):
            for j in range(d):
                for k in range(d):
                    for l in range(d):
                        s[k * d + l, i * d + j] = choi[i * d + k, j * d + l]
        return s

    def superop_to_choi(s):
        choi = np.zeros((d * d, d * d), dtype=complex)
        for i in range(d):
            for j in range(d):
                for k in range(d):
                    for l in range(d):
                        choi[i * d + k, j * d + l] = s[k * d + l, i * d + j]
        return choi

    sa = choi_to_superop(choi_a)
    sb = choi_to_superop(choi_b)
    sc = sb @ sa
    return superop_to_choi(sc)


def initialize_adjoint_and_compose(data1, data2):
    choi1 = _to_choi(data1)
    choi2 = _to_choi(data2)
    adjoint_choi1 = _adjoint_choi(choi1)
    composed_choi = _compose_choi(choi1, choi2)
    return choi1, adjoint_choi1, composed_choi
