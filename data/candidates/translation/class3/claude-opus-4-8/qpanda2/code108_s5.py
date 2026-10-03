# EVAL_META: task_id=108, framework=qpanda2, class=3
import numpy as np
from pyqpanda import CPUQVM

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(4)


def _to_choi(data):
    data = np.asarray(data, dtype=complex)
    dim = int(round(np.sqrt(data.shape[0])))
    if data.shape[0] == data.shape[1] and abs(data.shape[0] - dim * dim) < 1e-9 and dim * dim == data.shape[0]:
        return data
    d_out, d_in = data.shape
    choi = np.zeros((d_in * d_out, d_in * d_out), dtype=complex)
    for i in range(d_in):
        for j in range(d_in):
            eij = np.zeros((d_in, d_in), dtype=complex)
            eij[i, j] = 1.0
            mapped = data @ eij @ data.conj().T
            choi += np.kron(eij, mapped)
    return choi


def _choi_adjoint(choi):
    dim = int(round(np.sqrt(choi.shape[0])))
    d_row = dim
    d_col = dim
    conj = choi.conj().T
    result = np.zeros_like(choi)
    for a in range(d_row):
        for b in range(d_col):
            for c in range(d_row):
                for d in range(d_col):
                    result[a * d_col + b, c * d_col + d] = conj[b * d_row + a, d * d_row + c]
    return result


def _choi_to_kraus(choi):
    dim = int(round(np.sqrt(choi.shape[0])))
    vals, vecs = np.linalg.eigh(choi)
    kraus = []
    for k in range(len(vals)):
        if vals[k] > 1e-12:
            vec = np.sqrt(vals[k]) * vecs[:, k]
            kraus.append(vec.reshape(dim, dim).T)
    return kraus


def _choi_compose(choi1, choi2):
    kraus1 = _choi_to_kraus(choi1)
    kraus2 = _choi_to_kraus(choi2)
    dim = int(round(np.sqrt(choi1.shape[0])))
    composed = np.zeros((dim * dim, dim * dim), dtype=complex)
    for k1 in kraus1:
        for k2 in kraus2:
            k = k2 @ k1
            vec = np.zeros(dim * dim, dtype=complex)
            for i in range(dim):
                for j in range(dim):
                    vec[i * dim + j] = k[j, i]
            composed += np.outer(vec, vec.conj())
    return composed


def initialize_adjoint_and_compose(data1, data2):
    choi1 = _to_choi(data1)
    choi2 = _to_choi(data2)
    adjoint_choi1 = _choi_adjoint(choi1)
    composed_choi = _choi_compose(choi1, choi2)
    return choi1, adjoint_choi1, composed_choi


machine.finalize()
