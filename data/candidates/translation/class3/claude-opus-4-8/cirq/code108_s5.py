# EVAL_META: task_id=108, framework=cirq, class=3
import numpy as np


def _to_choi(data):
    arr = np.asarray(data, dtype=complex)
    if arr.ndim == 2:
        dim = int(round(np.sqrt(arr.shape[0])))
        if dim * dim == arr.shape[0] and arr.shape[0] == arr.shape[1]:
            return arr.copy()
        d_out, d_in = arr.shape
        choi = np.zeros((d_in * d_out, d_in * d_out), dtype=complex)
        for i in range(d_in):
            for j in range(d_in):
                block = np.outer(arr[:, i], np.conj(arr[:, j]))
                choi[i * d_out:(i + 1) * d_out, j * d_out:(j + 1) * d_out] = block
        return choi
    raise ValueError("Unsupported data format")


def _choi_dims(choi):
    d = int(round(np.sqrt(choi.shape[0])))
    return d, d


def _adjoint_choi(choi):
    d_in, d_out = _choi_dims(choi)
    result = np.zeros_like(choi)
    for a in range(d_in):
        for b in range(d_in):
            for c in range(d_out):
                for e in range(d_out):
                    result[c * d_in + a, e * d_in + b] = np.conj(
                        choi[a * d_out + c, b * d_out + e]
                    )
    return result


def _compose_choi(choi1, choi2):
    d1_in, d1_out = _choi_dims(choi1)
    d2_in, d2_out = _choi_dims(choi2)
    result = np.zeros((d1_in * d2_out, d1_in * d2_out), dtype=complex)
    for a in range(d1_in):
        for b in range(d1_in):
            for x in range(d2_out):
                for y in range(d2_out):
                    total = 0.0 + 0.0j
                    for k in range(d1_out):
                        c1 = choi1[a * d1_out + k, b * d1_out + k]
                    for k in range(d1_out):
                        for l in range(d1_out):
                            total += choi1[a * d1_out + k, b * d1_out + l] * \
                                choi2[k * d2_out + x, l * d2_out + y]
                    result[a * d2_out + x, b * d2_out + y] = total
    return result


def initialize_adjoint_and_compose(data1, data2):
    choi1 = _to_choi(data1)
    choi2 = _to_choi(data2)
    adjoint_choi1 = _adjoint_choi(choi1)
    composed_choi = _compose_choi(choi1, choi2)
    return choi1, adjoint_choi1, composed_choi
