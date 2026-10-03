# EVAL_META: task_id=108, framework=cirq, class=3
import numpy as np


class Choi:
    def __init__(self, data):
        if isinstance(data, Choi):
            self._data = np.array(data._data, dtype=complex)
            self._input_dim = data._input_dim
            self._output_dim = data._output_dim
        else:
            arr = np.array(data, dtype=complex)
            if arr.ndim == 2 and arr.shape[0] == arr.shape[1]:
                total = arr.shape[0]
                d = int(round(np.sqrt(total)))
                if d * d == total:
                    self._data = arr
                    self._input_dim = d
                    self._output_dim = d
                    return
            self._data, self._input_dim, self._output_dim = self._from_operator(arr)

    @staticmethod
    def _from_operator(u):
        dim = u.shape[0]
        choi = np.zeros((dim * dim, dim * dim), dtype=complex)
        for i in range(dim):
            for j in range(dim):
                e = np.zeros((dim, dim), dtype=complex)
                e[i, j] = 1.0
                conj = u @ e @ u.conj().T
                choi += np.kron(e, conj)
        return choi, dim, dim

    @property
    def data(self):
        return self._data

    def adjoint(self):
        din = self._input_dim
        dout = self._output_dim
        choi = self._data
        new = np.zeros_like(choi)
        for i in range(din):
            for j in range(din):
                for k in range(dout):
                    for l in range(dout):
                        row = i * dout + k
                        col = j * dout + l
                        nrow = k * din + i
                        ncol = l * din + j
                        new[nrow, ncol] = np.conj(choi[col, row])
        result = Choi.__new__(Choi)
        result._data = new
        result._input_dim = dout
        result._output_dim = din
        return result

    def _to_superop(self):
        din = self._input_dim
        dout = self._output_dim
        choi = self._data
        sup = np.zeros((dout * dout, din * din), dtype=complex)
        for i in range(din):
            for j in range(din):
                for k in range(dout):
                    for l in range(dout):
                        crow = i * dout + k
                        ccol = j * dout + l
                        srow = k * dout + l
                        scol = i * din + j
                        sup[srow, scol] = choi[crow, ccol]
        return sup, din, dout

    @staticmethod
    def _from_superop(sup, din, dout):
        choi = np.zeros((din * dout, din * dout), dtype=complex)
        for i in range(din):
            for j in range(din):
                for k in range(dout):
                    for l in range(dout):
                        crow = i * dout + k
                        ccol = j * dout + l
                        srow = k * dout + l
                        scol = i * din + j
                        choi[crow, ccol] = sup[srow, scol]
        return choi

    def compose(self, other):
        sup1, din1, dout1 = self._to_superop()
        sup2, din2, dout2 = other._to_superop()
        sup = sup2 @ sup1
        choi = Choi._from_superop(sup, din1, dout2)
        result = Choi.__new__(Choi)
        result._data = choi
        result._input_dim = din1
        result._output_dim = dout2
        return result


def initialize_adjoint_and_compose(data1, data2):
    choi1 = Choi(data1)
    choi2 = Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi
