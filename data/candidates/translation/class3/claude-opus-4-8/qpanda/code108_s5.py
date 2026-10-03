# EVAL_META: task_id=108, framework=qpanda, class=3
import numpy as np


def _to_choi(data):
    arr = np.asarray(data, dtype=complex)
    n = arr.shape[0]
    d = int(round(np.sqrt(n)))
    if d * d == n:
        return arr
    dim = arr.shape[0]
    choi = np.zeros((dim * dim, dim * dim), dtype=complex)
    for i in range(dim):
        for j in range(dim):
            e = np.zeros((dim, dim), dtype=complex)
            e[i, j] = 1.0
            mapped = arr @ e @ arr.conj().T
            choi += np.kron(e, mapped)
    return choi


def _choi_dims(choi):
    d = int(round(np.sqrt(choi.shape[0])))
    return d, d


def _choi_adjoint(choi):
    d_in, d_out = _choi_dims(choi)
    result = np.zeros_like(choi)
    for i in range(d_in):
        for j in range(d_in):
            block = choi[i * d_out:(i + 1) * d_out, j * d_out:(j + 1) * d_out]
            result[j * d_out:(j + 1) * d_out, i * d_out:(i + 1) * d_out] = block.conj().T
    return result


def _choi_to_superop(choi):
    d_in, d_out = _choi_dims(choi)
    superop = np.zeros((d_out * d_out, d_in * d_in), dtype=complex)
    for a in range(d_in):
        for b in range(d_in):
            block = choi[a * d_out:(a + 1) * d_out, b * d_out:(b + 1) * d_out]
            for c in range(d_out):
                for dd in range(d_out):
                    row = c * d_out + dd
                    col = a * d_in + b
                    superop[row, col] = block[c, dd]
    return superop, d_in, d_out


def _superop_to_choi(superop, d_in, d_out):
    choi = np.zeros((d_in * d_out, d_in * d_out), dtype=complex)
    for a in range(d_in):
        for b in range(d_in):
            col = a * d_in + b
            for c in range(d_out):
                for dd in range(d_out):
                    row = c * d_out + dd
                    choi[a * d_out + c, b * d_out + dd] = superop[row, col]
    return choi


def _choi_compose(choi1, choi2):
    s1, d1_in, d1_out = _choi_to_superop(choi1)
    s2, d2_in, d2_out = _choi_to_superop(choi2)
    composed = s2 @ s1
    return _superop_to_choi(composed, d1_in, d2_out)


def initialize_adjoint_and_compose(data1, data2):
    choi1 = _to_choi(data1)
    choi2 = _to_choi(data2)
    adjoint_choi1 = _choi_adjoint(choi1)
    composed_choi = _choi_compose(choi1, choi2)
    return choi1, adjoint_choi1, composed_choi
