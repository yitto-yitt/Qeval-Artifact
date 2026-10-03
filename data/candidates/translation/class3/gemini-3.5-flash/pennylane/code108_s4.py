# EVAL_META: task_id=108, framework=pennylane, class=3
import pennylane as qml
import numpy as np


class Choi:
    def __init__(self, data):
        if isinstance(data, Choi):
            self.matrix = np.array(data.matrix)
        else:
            self.matrix = np.array(data)
        sz = self.matrix.shape[0]
        self.d = int(np.round(np.sqrt(sz)))

    @property
    def data(self):
        return self.matrix

    def __array__(self):
        return self.matrix

    def to_superop(self):
        d = self.d
        tensor = self.matrix.reshape(d, d, d, d)
        superop_tensor = np.transpose(tensor, (3, 1, 2, 0))
        return superop_tensor.reshape(d * d, d * d)

    @classmethod
    def from_superop(cls, superop):
        sz = superop.shape[0]
        d = int(np.round(np.sqrt(sz)))
        tensor = superop.reshape(d, d, d, d)
        choi_tensor = np.transpose(tensor, (3, 1, 2, 0))
        return cls(choi_tensor.reshape(d * d, d * d))

    def adjoint(self):
        S = self.to_superop()
        S_adj = np.conjugate(S.T)
        return Choi.from_superop(S_adj)

    def compose(self, other):
        if not isinstance(other, Choi):
            other = Choi(other)
        S1 = self.to_superop()
        S2 = other.to_superop()
        S_comp = S2 @ S1
        return Choi.from_superop(S_comp)


def initialize_adjoint_and_compose(data1, data2):
    choi1 = Choi(data1)
    choi2 = Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi
