# EVAL_META: task_id=108, framework=qpanda, class=3
import numpy as np

class Choi:
    def __init__(self, data):
        self.data = np.array(data, dtype=complex)
        
    def adjoint(self):
        return Choi(self.data.conj().T)
        
    def compose(self, other):
        d = int(np.round(np.sqrt(self.data.shape[0])))
        J1 = self.data.reshape(d, d, d, d)
        S1 = np.transpose(J1, (1, 3, 0, 2)).reshape(d**2, d**2)
        
        J2 = other.data.reshape(d, d, d, d)
        S2 = np.transpose(J2, (1, 3, 0, 2)).reshape(d**2, d**2)
        
        S_comp = S2 @ S1
        
        J_comp = np.transpose(S_comp.reshape(d, d, d, d), (2, 0, 3, 1)).reshape(d**2, d**2)
        return Choi(J_comp)

def initialize_adjoint_and_compose(data1, data2):
    choi1 = Choi(data1)
    choi2 = Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi
