# EVAL_META: task_id=108, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq


class Choi:

    def __init__(self, data):
        if isinstance(data, Choi):
            self.data = np.array(data.data, dtype=complex)
        else:
            self.data = np.array(data, dtype=complex)
        self.dim = int(np.sqrt(self.data.shape[0]))

    def adjoint(self):
        d = self.dim
        reshaped = self.data.reshape(d, d, d, d)
        swapped = np.transpose(reshaped, (1, 0, 3, 2))
        adj_data = np.conj(swapped).reshape(d * d, d * d)
        return Choi(adj_data)

    def compose(self, other):
        if not isinstance(other, Choi):
            other = Choi(other)
        d = self.dim
        K1 = np.transpose(self.data.reshape(d, d, d, d), (1, 3, 0, 2)).reshape(
            d * d, d * d
        )
        K2 = np.transpose(
            other.data.reshape(d, d, d, d), (1, 3, 0, 2)
        ).reshape(d * d, d * d)
        K = K2 @ K1
        J = np.transpose(K.reshape(d, d, d, d), (2, 0, 3, 1)).reshape(
            d * d, d * d
        )
        return Choi(J)


def initialize_adjoint_and_compose(data1, data2):
    try:
        qvm = pq.CPUQVM()
        qvm.init_qvm()
        qvm.finalize()
    except:
        pass
    choi1 = Choi(data1)
    choi2 = Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi
