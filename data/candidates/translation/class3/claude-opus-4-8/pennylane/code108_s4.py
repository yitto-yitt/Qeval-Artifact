# EVAL_META: task_id=108, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def _choi_to_kraus(choi, d_in, d_out):
    choi = (choi + choi.conj().T) / 2.0
    vals, vecs = np.linalg.eigh(choi)
    tol = 1e-12 * max(1.0, np.max(np.abs(vals)) if vals.size else 1.0)
    kraus = []
    for i in range(len(vals)):
        val = vals[i]
        if val <= tol:
            continue
        vec = vecs[:, i] * np.sqrt(val)
        # vec index (i_in*d_out + i_out) = K[i_out, i_in]
        K = vec.reshape(d_in, d_out).T
        kraus.append(K)
    if not kraus:
        kraus = [np.zeros((d_out, d_in), dtype=complex)]
    return kraus


def _kraus_to_choi(kraus, d_in, d_out):
    choi = np.zeros((d_in * d_out, d_in * d_out), dtype=complex)
    for K in kraus:
        phi = K.T.reshape(-1)
        choi += np.outer(phi, phi.conj())
    return choi


class Choi:
    def __init__(self, data, input_dims=None, output_dims=None):
        if isinstance(data, Choi):
            self._data = np.array(data._data, dtype=complex)
            self._input_dim = data._input_dim
            self._output_dim = data._output_dim
            return
        mat = np.asarray(data, dtype=complex)
        n = mat.shape[0]
        if input_dims is None or output_dims is None:
            d = int(round(np.sqrt(n)))
            input_dims = d
            output_dims = d
        self._data = mat
        self._input_dim = int(input_dims)
        self._output_dim = int(output_dims)

    @property
    def data(self):
        return self._data

    def adjoint(self):
        kraus = _choi_to_kraus(self._data, self._input_dim, self._output_dim)
        adj = [K.conj().T for K in kraus]
        new_choi = _kraus_to_choi(adj, self._output_dim, self._input_dim)
        return Choi(new_choi, self._output_dim, self._input_dim)

    def compose(self, other, front=False):
        k_self = _choi_to_kraus(self._data, self._input_dim, self._output_dim)
        k_other = _choi_to_kraus(other._data, other._input_dim, other._output_dim)
        if front:
            kraus = [a @ b for a in k_self for b in k_other]
            din, dout = other._input_dim, self._output_dim
        else:
            kraus = [b @ a for a in k_self for b in k_other]
            din, dout = self._input_dim, other._output_dim
        new_choi = _kraus_to_choi(kraus, din, dout)
        return Choi(new_choi, din, dout)


def initialize_adjoint_and_compose(data1, data2):
    choi1 = Choi(data1)
    choi2 = Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi
