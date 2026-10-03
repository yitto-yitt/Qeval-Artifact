# EVAL_META: task_id=108, framework=pennylane, class=3
import numpy as np
import pennylane as qml


class Choi:
    def __init__(self, data):
        self._data = np.array(data, dtype=complex)

    def adjoint(self):
        return Choi(self._data.conj().T)

    def compose(self, other):
        return Choi(self._data @ other._data)


def initialize_adjoint_and_compose(data1, data2):
    choi1 = Choi(data1)
    choi2 = Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi
