# EVAL_META: task_id=108, framework=pennylane, class=3
import numpy as np
import pennylane as qml


class Choi:

    def __init__(self, data):
        if isinstance(data, Choi):
            self.data = np.array(data.data)
        else:
            self.data = np.array(data)
        self.dim = int(np.round(np.sqrt(self.data.shape[0])))

    def adjoint(self):
        d = self.dim
        reshaped = self.data.reshape(d, d, d, d)
        adj_data = np.transpose(reshaped.conj(), (1, 0, 3, 2)).reshape(
            d * d, d * d
        )
        return Choi(adj_data)

    def compose(self, other):
        if not isinstance(other, Choi):
            other = Choi(other)
        d = self.dim
        J2_reshaped = other.data.reshape(d, d, d, d)
        J1_reshaped = self.data.reshape(d, d, d, d)
        composed_data = np.einsum("abxy,bcyz->acxz", J2_reshaped, J1_reshaped)
        return Choi(composed_data.reshape(d * d, d * d))

    def __array__(self):
        return self.data


def initialize_adjoint_and_compose(data1, data2):
    choi1 = Choi(data1)
    choi2 = Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi
