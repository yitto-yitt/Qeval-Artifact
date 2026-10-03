# EVAL_META: task_id=108, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QStat, QMatrixXcd


class Choi:
    def __init__(self, data):
        self.data = np.array(data, dtype=complex)

    def adjoint(self):
        return Choi(self.data.conj().T)

    def compose(self, other):
        return Choi(np.dot(self.data, other.data))

    def to_qmatrix(self):
        return QMatrixXcd(self.data.tolist())

    def to_qstat(self):
        return QStat(self.data.flatten().tolist())


def initialize_adjoint_and_compose(data1, data2):
    choi1 = Choi(data1)
    choi2 = Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi
