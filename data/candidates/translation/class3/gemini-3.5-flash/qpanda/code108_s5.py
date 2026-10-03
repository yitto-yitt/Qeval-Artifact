# EVAL_META: task_id=108, framework=qpanda, class=3
import numpy as np
import pyqpanda as pq


class Choi:

    def __init__(self, data):
        if isinstance(data, Choi):
            self.data = np.array(data.data, dtype=complex)
        else:
            self.data = np.array(data, dtype=complex)
        n = self.data.shape[0]
        self.dim = int(np.sqrt(n))

    def adjoint(self):
        d = self.dim
        tensor = self.data.reshape(d, d, d, d)
        tensor_conj = np.conj(tensor)
        tensor_adj = np.transpose(tensor_conj, (1, 0, 3, 2))
        return Choi(tensor_adj.reshape(d * d, d * d))

    def compose(self, other):
        if not isinstance(other, Choi):
            other = Choi(other)
        d = self.dim
        j1 = self.data.reshape(d, d, d, d)
        j2 = other.data.reshape(d, d, d, d)
        j_composed = np.einsum("ikjl,kohq->iojq", j1, j2)
        return Choi(j_composed.reshape(d * d, d * d))

    @property
    def rvalue(self):
        return self.data

    def __array__(self):
        return self.data

    def __repr__(self):
        return f"Choi({self.data.tolist()})"


def initialize_adjoint_and_compose(data1, data2):
    choi1 = Choi(data1)
    choi2 = Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi
