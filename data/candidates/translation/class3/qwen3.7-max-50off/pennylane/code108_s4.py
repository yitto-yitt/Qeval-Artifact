# EVAL_META: task_id=108, framework=pennylane, class=3
import numpy as np

class Choi:
    def __init__(self, data):
        data = np.array(data, dtype=complex)
        if data.ndim == 2:
            d2 = data.shape[0]
            d = int(np.round(np.sqrt(d2)))
            if d * d == d2:
                self.data = data
            else:
                d = data.shape[0]
                C = np.einsum('ki,lj->ijkl', data, data.conj())
                self.data = C.reshape((d**2, d**2))
        else:
            self.data = data
            
    def adjoint(self):
        return Choi(self.data.conj().T)
        
    def compose(self, other):
        d2 = self.data.shape[0]
        d = int(np.round(np.sqrt(d2)))
        C1 = self.data.reshape((d, d, d, d))
        C2 = other.data.reshape((d, d, d, d))
        C12 = np.einsum('ijkl,klmn->ijmn', C1, C2)
        return Choi(C12.reshape((d2, d2)))

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
