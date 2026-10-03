# EVAL_META: task_id=108, framework=qpanda, class=3
import numpy as np


def _to_choi(data):
    arr = np.asarray(data, dtype=complex)
    n = arr.shape[0]
    d = int(round(np.sqrt(n)))
    if d * d == n and arr.shape[0] == arr.shape[1]:
        # Heuristic: treat as Choi if it looks like one already is ambiguous;
        # attempt to interpret as a unitary/superop -> Choi.
        pass
    return arr


def _unitary_to_choi(u):
    u = np.asarray(u, dtype=complex)
    d = u.shape[0]
    vec = u.reshape(d * d, 1, order='F')
    return vec @ vec.conj().T


def _superop_to_choi(s, dim):
    s = np.asarray(s, dtype=complex)
    choi = np.zeros((dim * dim, dim * dim), dtype=complex)
    for i in range(dim):
        for j in range(dim):
            # basis |i><j| flattened column-major
            e = np.zeros((dim * dim, 1), dtype=complex)
            e[j * dim + i, 0] = 1.0
            out = (s @ e).reshape(dim, dim, order='F')
            for k in range(dim):
                for l in range(dim):
                    choi[k * dim + i, l * dim + j] += out[k, l]
    return choi


def _make_choi(data):
    arr = np.asarray(data, dtype=complex)
    n = arr.shape[0]
    m = arr.shape[1]
    d = int(round(np.sqrt(n)))
    if d * d == n and n == m:
        # Could be a superoperator (d^2 x d^2). Convert superop -> Choi.
        return _superop_to_choi(arr, d)
    else:
        # Treat as unitary.
        return _unitary_to_choi(arr)


class ChoiObj:
    def __init__(self, data):
        if isinstance(data, ChoiObj):
            self.data = data.data.copy()
            self.dim = data.dim
        else:
            arr = np.asarray(data, dtype=complex)
            n = arr.shape[0]
            d = int(round(np.sqrt(n)))
            if d * d == n and arr.shape[0] == arr.shape[1]:
                # Ambiguity: assume input is a unitary matrix of size d0 x d0
                # unless it is exactly a Choi matrix. We convert unitary -> Choi.
                self.data = _make_choi(arr)
                self.dim = int(round(np.sqrt(self.data.shape[0])))
            else:
                self.data = _make_choi(arr)
                self.dim = int(round(np.sqrt(self.data.shape[0])))

    def adjoint(self):
        d = self.dim
        # Reindex Choi for adjoint channel.
        choi = self.data.reshape(d, d, d, d)
        # Choi_adj[(i,k),(j,l)] via swapping input/output and conjugation
        adj = np.zeros_like(self.data)
        new = choi.transpose(1, 0, 3, 2).conj()
        adj = new.reshape(d * d, d * d)
        out = ChoiObj.__new__(ChoiObj)
        out.data = adj
        out.dim = d
        return out

    def _to_superop(self):
        d = self.dim
        choi = self.data.reshape(d, d, d, d)
        superop = np.zeros((d * d, d * d), dtype=complex)
        for i in range(d):
            for k in range(d):
                for j in range(d):
                    for l in range(d):
                        # Choi index (i*d+k, j*d+l) -> superop (k*d+l, i*d+j)
                        superop[k * d + l, i * d + j] = choi[i, k, j, l]
        return superop

    def compose(self, other):
        d = self.dim
        s1 = self._to_superop()
        s2 = other._to_superop()
        s_comp = s2 @ s1
        choi = _superop_to_choi(s_comp, d)
        out = ChoiObj.__new__(ChoiObj)
        out.data = choi
        out.dim = d
        return out


def initialize_adjoint_and_compose(data1, data2):
    choi1 = ChoiObj(data1)
    choi2 = ChoiObj(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi
