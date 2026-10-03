# EVAL_META: task_id=108, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def _choi_from_kraus(kraus, din, dout):
    dim = din * dout
    C = np.zeros((dim, dim), dtype=complex)
    for K in kraus:
        v = np.asarray(K, dtype=complex).flatten(order='F')
        C += np.outer(v, v.conj())
    return C


class Choi:
    def __init__(self, data):
        if isinstance(data, Choi):
            self._data = np.array(data._data, dtype=complex)
            self._din = data._din
            self._dout = data._dout
            return
        arr = np.array(data, dtype=complex)
        if arr.ndim == 3:
            # list of Kraus operators (dout x din)
            dout, din = arr.shape[1], arr.shape[2]
            self._data = _choi_from_kraus([arr[i] for i in range(arr.shape[0])], din, dout)
            self._din = din
            self._dout = dout
        else:
            self._data = arr
            dim = arr.shape[0]
            d = int(round(np.sqrt(dim)))
            self._din = d
            self._dout = d

    @property
    def data(self):
        return self._data

    def __array__(self, dtype=None):
        return np.array(self._data, dtype=dtype)

    def __eq__(self, other):
        try:
            return np.allclose(self._data, np.array(other, dtype=complex))
        except Exception:
            return NotImplemented

    def _to_kraus(self):
        vals, vecs = np.linalg.eigh(self._data)
        din, dout = self._din, self._dout
        kraus = []
        for i in range(len(vals)):
            lam = vals[i]
            if abs(lam) < 1e-12:
                continue
            v = vecs[:, i] * np.sqrt(complex(lam))
            K = v.reshape(din, dout).T
            kraus.append(K)
        return kraus

    def adjoint(self):
        kraus = self._to_kraus()
        adj = [K.conj().T for K in kraus]
        return Choi(_choi_from_kraus(adj, self._dout, self._din))

    def compose(self, other, front=False):
        A = self._to_kraus()
        B = other._to_kraus()
        if front:
            new = [a @ b for a in A for b in B]
            din, dout = other._din, self._dout
        else:
            new = [b @ a for a in A for b in B]
            din, dout = self._din, other._dout
        return Choi(_choi_from_kraus(new, din, dout))


def initialize_adjoint_and_compose(data1, data2):
    choi1 = Choi(data1)
    choi2 = Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi
