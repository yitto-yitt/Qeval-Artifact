# EVAL_META: task_id=108, framework=pennylane, class=3
import numpy as np


def _to_choi(data):
    arr = np.asarray(data, dtype=complex)
    dim = arr.shape[0]
    if arr.shape[0] == arr.shape[1] and _is_unitary(arr):
        d = arr.shape[0]
        vec = arr.reshape(-1, order='F')
        choi = np.outer(vec, vec.conj())
        return choi, d, d
    return arr, int(round(np.sqrt(dim))), int(round(np.sqrt(dim)))


def _is_unitary(arr):
    if arr.shape[0] != arr.shape[1]:
        return False
    d = arr.shape[0]
    return np.allclose(arr.conj().T @ arr, np.eye(d))


class Choi:
    def __init__(self, data):
        if isinstance(data, Choi):
            self._data = data._data.copy()
            self._input_dim = data._input_dim
            self._output_dim = data._output_dim
        else:
            mat, idim, odim = _to_choi(data)
            self._data = mat
            self._input_dim = idim
            self._output_dim = odim

    @property
    def data(self):
        return self._data

    def adjoint(self):
        din = self._input_dim
        dout = self._output_dim
        c = self._data.reshape(din, dout, din, dout)
        c = c.conj()
        c = np.transpose(c, (1, 0, 3, 2))
        new = c.reshape(dout * din, dout * din)
        out = Choi.__new__(Choi)
        out._data = new
        out._input_dim = dout
        out._output_dim = din
        return out

    def compose(self, other, front=False):
        if not isinstance(other, Choi):
            other = Choi(other)
        if front:
            first, second = other, self
        else:
            first, second = self, other

        da_in = first._input_dim
        da_out = first._output_dim
        db_in = second._input_dim
        db_out = second._output_dim

        A = first._data.reshape(da_in, da_out, da_in, da_out)
        B = second._data.reshape(db_in, db_out, db_in, db_out)

        # A maps da_in -> da_out, B maps db_in (=da_out) -> db_out
        result = np.einsum('ijkl,jmln->imkn', A, B)
        new = result.reshape(da_in * db_out, da_in * db_out)
        out = Choi.__new__(Choi)
        out._data = new
        out._input_dim = da_in
        out._output_dim = db_out
        return out

    def __array__(self):
        return self._data

    def __repr__(self):
        return f"Choi({self._data})"


def initialize_adjoint_and_compose(data1, data2):
    choi1 = Choi(data1)
    choi2 = Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi
