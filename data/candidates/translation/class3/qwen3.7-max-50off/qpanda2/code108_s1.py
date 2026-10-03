# EVAL_META: task_id=108, framework=qpanda2, class=3
import numpy as np
from pyqpanda import CPUQVM

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

class Choi:
    def __init__(self, data):
        self.data = np.array(data, dtype=complex)
        
    def adjoint(self):
        return Choi(self.data.conj().T)
        
    def compose(self, other):
        d2 = self.data.shape[0]
        d = int(np.sqrt(d2))
        
        C1 = self.data.reshape(d, d, d, d)
        S1 = C1.transpose(0, 2, 1, 3).reshape(d2, d2)
        
        C2 = other.data.reshape(d, d, d, d)
        S2 = C2.transpose(0, 2, 1, 3).reshape(d2, d2)
        
        S_comp = S1 @ S2
        
        C_comp = S_comp.reshape(d, d, d, d).transpose(0, 2, 1, 3).reshape(d2, d2)
        
        return Choi(C_comp)

    def __array__(self, dtype=None):
        if dtype is not None:
            return self.data.astype(dtype)
        return self.data

def initialize_adjoint_and_compose(data1, data2):
    choi1 = Choi(data1)
    choi2 = Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi

machine.finalize()
