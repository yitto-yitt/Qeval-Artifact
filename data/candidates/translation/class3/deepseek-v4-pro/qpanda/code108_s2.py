# EVAL_META: task_id=108, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import *


class Choi:
    """Minimal Choi-matrix container mirroring the Qiskit API used here."""
    def __init__(self, data):
        if isinstance(data, Choi):
            self.data = data.data.copy()
        else:
            self.data = np.asarray(data, dtype=complex).copy()

    def adjoint(self):
        return Choi(np.conj(self.data.T))

    def compose(self, other, front=False):
        if not isinstance(other, Choi):
            other = Choi(other)
        s_self = _choi_to_superop(self.data)
        s_other = _choi_to_superop(other.data)
        if front:
            s = s_self @ s_other
        else:
            s = s_other @ s_self
        return Choi(_superop_to_choi(s))

    def __array__(self, dtype=None):
        return np.asarray(self.data, dtype=dtype)


def _choi_to_superop(choi):
    mat = np.asarray(choi, dtype=complex)
    d = int(np.sqrt(mat.shape[0]))
    c4 = mat.reshape(d, d, d, d)
    s4 = np.conj(np.transpose(c4, (0, 2, 1, 3)))
    return s4.reshape(d * d, d * d)


def _superop_to_choi(superop):
    mat = np.asarray(superop, dtype=complex)
    d_out = int(np.sqrt(mat.shape[0]))
    d_in = int(np.sqrt(mat.shape[1]))
    s4 = mat.reshape(d_out, d_out, d_in, d_in)
    c4 = np.conj(np.transpose(s4, (0, 2, 1, 3)))
    return c4.reshape(d_out * d_in, d_out * d_in)


def initialize_adjoint_and_compose(data1, data2):
    choi1 = Choi(data1)
    choi2 = Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi
