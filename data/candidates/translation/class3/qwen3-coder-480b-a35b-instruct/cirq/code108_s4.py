# EVAL_META: task_id=108, framework=cirq, class=3
import numpy as np
import cirq


class ChoiMatrix:
    def __init__(self, data):
        self.data = np.array(data)
    
    def adjoint(self):
        # For Choi matrix, adjoint is conjugate transpose
        return ChoiMatrix(self.data.conj().T)
    
    def compose(self, other):
        # Matrix multiplication for composing Choi matrices
        return ChoiMatrix(np.dot(self.data, other.data))


def initialize_adjoint_and_compose(data1, data2):
    choi1 = ChoiMatrix(data1)
    choi2 = ChoiMatrix(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi
