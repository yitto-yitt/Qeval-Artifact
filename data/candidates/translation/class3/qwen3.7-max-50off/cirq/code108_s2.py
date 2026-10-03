# EVAL_META: task_id=108, framework=cirq, class=3
import numpy as np

class Choi:
    def __init__(self, data):
        self.data = np.array(data, dtype=complex)
        
    def adjoint(self):
        return Choi(self.data.conj().T)
        
    def compose(self, other):
        d = int(np.sqrt(self.data.shape[0]))
        S1 = np.transpose(self.data.reshape(d, d, d, d), (2, 3, 0, 1)).reshape(d**2, d**2)
        S2 = np.transpose(other.data.reshape(d, d, d, d), (2, 3, 0, 1)).reshape(d**2, d**2)
        S12 = S2 @ S1
        C12 = np.transpose(S12.reshape(d, d, d, d), (2, 3, 0, 1)).reshape(d**2, d**2)
        return Choi(C12)

def initialize_adjoint_and_compose(data1, data2):
    choi1 = Choi(data1)
    choi2 = Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi
