# EVAL_META: task_id=108, framework=cirq, class=3
import numpy as np


def _to_choi(data):
    if hasattr(data, "_choi_matrix"):
        return _Choi(np.array(data._choi_matrix, dtype=complex))
    if isinstance(data, _Choi):
        return _Choi(np.array(data._choi_matrix, dtype=complex))
    arr = np.array(data, dtype=complex)
    if arr.ndim == 2 and arr.shape[0] == arr.shape[1]:
        d = int(round(np.sqrt(arr.shape[0])))
        if d * d == arr.shape[0]:
            return _Choi(arr.copy())
    return _from_kraus(_as_kraus(data))


def _as_kraus(data):
    arr = np.array(data, dtype=complex)
    if arr.ndim == 2:
        return [arr]
    if arr.ndim == 3:
        return [arr[i] for i in range(arr.shape[0])]
    raise ValueError("Unsupported data for Choi initialization")


def _from_kraus(kraus):
    d = kraus[0].shape[1]
    choi = np.zeros((d * d, d * d), dtype=complex)
    for k in kraus:
        v = k.reshape(-1, 1, order="F")
        choi += v @ v.conj().T
    return _Choi(choi)


class _Choi:
    def __init__(self, matrix):
        self._choi_matrix = np.array(matrix, dtype=complex)
        self.dim = int(round(np.sqrt(self._choi_matrix.shape[0])))

    @property
    def data(self):
        return self._choi_matrix

    def adjoint(self):
        d = self.dim
        m = self._choi_matrix.reshape(d, d, d, d)
        # Choi_adjoint = swap input/output and conjugate
        m_adj = np.conjugate(np.transpose(m, (1, 0, 3, 2)))
        return _Choi(m_adj.reshape(d * d, d * d))

    def _to_superop(self):
        d = self.dim
        c = self._choi_matrix.reshape(d, d, d, d)
        # Choi C_{ij,kl}; Superop S_{(i k),(j l)} via reshape convention
        s = np.transpose(c, (0, 2, 1, 3)).reshape(d * d, d * d)
        return s, d

    @staticmethod
    def _from_superop(s, d):
        sr = s.reshape(d, d, d, d)
        c = np.transpose(sr, (0, 2, 1, 3)).reshape(d * d, d * d)
        return _Choi(c)

    def compose(self, other, front=False):
        s1, d = self._to_superop()
        s2, _ = other._to_superop()
        if front:
            s = s1 @ s2
        else:
            s = s2 @ s1
        return _Choi._from_superop(s, d)


def initialize_adjoint_and_compose(data1, data2):
    choi1 = _to_choi(data1)
    choi2 = _to_choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi
