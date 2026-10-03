# EVAL_META: task_id=108, framework=pennylane, class=3
import numpy as np


def _reshuffle(mat, shape):
    return np.reshape(
        np.transpose(np.reshape(mat, shape), (3, 1, 2, 0)),
        (shape[3] * shape[1], shape[2] * shape[0]),
    )


def _superop_to_choi(data, input_dim, output_dim):
    shape = (output_dim, output_dim, input_dim, input_dim)
    return _reshuffle(data, shape)


def _choi_to_superop(data, input_dim, output_dim):
    shape = (input_dim, output_dim, input_dim, output_dim)
    return _reshuffle(data, shape)


class Choi:
    def __init__(self, data, input_dim=None, output_dim=None):
        if isinstance(data, Choi):
            self.data = np.array(data.data, dtype=complex)
            self.input_dim = data.input_dim
            self.output_dim = data.output_dim
            return
        arr = np.asarray(data, dtype=complex)
        self.data = arr
        dl, dr = arr.shape
        if input_dim is None or output_dim is None:
            d = int(round(np.sqrt(dl)))
            input_dim = d
            output_dim = int(round(dr / d)) if d != 0 else d
        self.input_dim = input_dim
        self.output_dim = output_dim

    def _to_superop(self):
        return _choi_to_superop(self.data, self.input_dim, self.output_dim)

    @staticmethod
    def _from_superop(superop, input_dim, output_dim):
        choi_mat = _superop_to_choi(superop, input_dim, output_dim)
        c = Choi(choi_mat, input_dim, output_dim)
        return c

    def adjoint(self):
        s = self._to_superop()
        s_adj = np.conj(s.T)
        return Choi._from_superop(s_adj, self.output_dim, self.input_dim)

    def compose(self, other, front=False):
        other = other if isinstance(other, Choi) else Choi(other)
        s_self = self._to_superop()
        s_other = other._to_superop()
        if front:
            s_comp = s_self @ s_other
            in_dim = other.input_dim
            out_dim = self.output_dim
        else:
            s_comp = s_other @ s_self
            in_dim = self.input_dim
            out_dim = other.output_dim
        return Choi._from_superop(s_comp, in_dim, out_dim)

    def __repr__(self):
        return "Choi(\n{})".format(self.data)


def initialize_adjoint_and_compose(data1, data2):
    choi1 = Choi(data1)
    choi2 = Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi
