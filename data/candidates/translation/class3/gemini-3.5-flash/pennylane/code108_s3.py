# EVAL_META: task_id=108, framework=pennylane, class=3
import math
import pennylane as qml


class Choi:

    def __init__(self, data):
        if isinstance(data, Choi):
            self.data = data.data
        else:
            self.data = data
        self.shape = qml.math.shape(self.data)
        self.dim = int(math.sqrt(self.shape[0]))

    def adjoint(self):
        d = self.dim
        tensor = qml.math.reshape(self.data, (d, d, d, d))
        tensor_conj = qml.math.conj(tensor)
        adj_tensor = qml.math.transpose(tensor_conj, (1, 0, 3, 2))
        return Choi(qml.math.reshape(adj_tensor, self.shape))

    def compose(self, other):
        if not isinstance(other, Choi):
            other = Choi(other)
        d = self.dim
        lambda1 = qml.math.reshape(self.data, (d, d, d, d))
        lambda2 = qml.math.reshape(other.data, (d, d, d, d))
        composed_tensor = qml.math.einsum("cadb,aebf->cedf", lambda1, lambda2)
        return Choi(qml.math.reshape(composed_tensor, self.shape))


def initialize_adjoint_and_compose(data1, data2):
    choi1 = Choi(data1)
    choi2 = Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi
