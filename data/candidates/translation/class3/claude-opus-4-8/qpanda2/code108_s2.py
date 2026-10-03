# EVAL_META: task_id=108, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(4)


def _to_choi(data):
    arr = np.array(data, dtype=complex)
    if arr.ndim == 2 and arr.shape[0] == arr.shape[1]:
        n = arr.shape[0]
        d = int(round(np.sqrt(n)))
        if d * d == n:
            # Could be a Choi already or a unitary; treat square matrix
            # If it's a unitary of dimension d, build Choi from it
            # Heuristic: if unitary (U U^dag = I), build Choi
            if np.allclose(arr.conj().T @ arr, np.eye(n)):
                return _choi_from_unitary(arr)
            else:
                # assume already a Choi matrix
                return arr
    # assume unitary
    return _choi_from_unitary(arr)


def _choi_from_unitary(u):
    d = u.shape[0]
    choi = np.zeros((d * d, d * d), dtype=complex)
    for i in range(d):
        for j in range(d):
            eij = np.zeros((d, d), dtype=complex)
            eij[i, j] = 1.0
            out = u @ eij @ u.conj().T
            choi += np.kron(eij, out)
    return choi


def _choi_to_kraus(choi, dim_in, dim_out):
    w, v = np.linalg.eigh(choi)
    kraus = []
    for idx in range(len(w)):
        lam = w[idx]
        if lam > 1e-12:
            vec = v[:, idx] * np.sqrt(lam)
            k = vec.reshape(dim_in, dim_out).T
            kraus.append(k)
    return kraus


def _kraus_to_choi(kraus, dim_in, dim_out):
    choi = np.zeros((dim_in * dim_out, dim_in * dim_out), dtype=complex)
    for i in range(dim_in):
        for j in range(dim_in):
            eij = np.zeros((dim_in, dim_in), dtype=complex)
            eij[i, j] = 1.0
            out = np.zeros((dim_out, dim_out), dtype=complex)
            for k in kraus:
                out += k @ eij @ k.conj().T
            choi += np.kron(eij, out)
    return choi


def _adjoint_choi(choi):
    d2 = choi.shape[0]
    d = int(round(np.sqrt(d2)))
    kraus = _choi_to_kraus(choi, d, d)
    adj_kraus = [k.conj().T for k in kraus]
    return _kraus_to_choi(adj_kraus, d, d)


def _compose_choi(choi1, choi2):
    d2 = choi1.shape[0]
    d = int(round(np.sqrt(d2)))
    k1 = _choi_to_kraus(choi1, d, d)
    k2 = _choi_to_kraus(choi2, d, d)
    composed = []
    for b in k2:
        for a in k1:
            composed.append(b @ a)
    return _kraus_to_choi(composed, d, d)


def initialize_adjoint_and_compose(data1, data2):
    choi1 = _to_choi(data1)
    choi2 = _to_choi(data2)
    adjoint_choi1 = _adjoint_choi(choi1)
    composed_choi = _compose_choi(choi1, choi2)
    return choi1, adjoint_choi1, composed_choi


machine.finalize()
