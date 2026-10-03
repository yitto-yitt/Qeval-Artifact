# EVAL_META: task_id=108, framework=qpanda2, class=3
import numpy as np
from pyqpanda import CPUQVM

machine = CPUQVM()
machine.init_qvm()
_qubits = machine.qAlloc_many(4)


def _to_choi(data):
    arr = np.array(data, dtype=complex)
    if arr.ndim == 2 and arr.shape[0] == arr.shape[1]:
        n = arr.shape[0]
        d = int(round(np.sqrt(n)))
        if d * d == n:
            # Check if it looks like a Choi matrix already (Hermitian)
            if np.allclose(arr, arr.conj().T):
                return arr
        # Treat as unitary / superoperator-defining matrix -> build Choi
        dim = arr.shape[0]
        d = int(round(np.sqrt(dim)))
        if d * d == dim:
            # superoperator to choi via reshuffle
            return _superop_to_choi(arr)
        else:
            # unitary matrix -> choi
            return _unitary_to_choi(arr)
    raise ValueError("Unsupported data format")


def _unitary_to_choi(U):
    d = U.shape[0]
    choi = np.zeros((d * d, d * d), dtype=complex)
    for i in range(d):
        for j in range(d):
            e_ij = np.zeros((d, d), dtype=complex)
            e_ij[i, j] = 1.0
            out = U @ e_ij @ U.conj().T
            choi += np.kron(e_ij, out)
    return choi


def _superop_to_choi(S):
    d = int(round(np.sqrt(S.shape[0])))
    choi = S.reshape(d, d, d, d)
    choi = choi.transpose(3, 1, 2, 0)
    choi = choi.reshape(d * d, d * d)
    return choi


def _choi_to_superop(choi):
    d = int(round(np.sqrt(choi.shape[0])))
    c = choi.reshape(d, d, d, d)
    s = c.transpose(3, 1, 2, 0)
    return s.reshape(d * d, d * d)


def _adjoint_choi(choi):
    d = int(round(np.sqrt(choi.shape[0])))
    S = _choi_to_superop(choi)
    S_adj = S.conj().T
    return _superop_to_choi(S_adj)


def _compose_choi(choi1, choi2):
    d = int(round(np.sqrt(choi1.shape[0])))
    S1 = _choi_to_superop(choi1)
    S2 = _choi_to_superop(choi2)
    S = S2 @ S1
    return _superop_to_choi(S)


def initialize_adjoint_and_compose(data1, data2):
    choi1 = _to_choi(data1)
    choi2 = _to_choi(data2)
    adjoint_choi1 = _adjoint_choi(choi1)
    composed_choi = _compose_choi(choi1, choi2)
    return choi1, adjoint_choi1, composed_choi


machine.finalize()
