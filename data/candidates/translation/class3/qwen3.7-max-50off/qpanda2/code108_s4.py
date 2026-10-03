# EVAL_META: task_id=108, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(4)

class Choi:
    def __init__(self, data):
        self.data = np.array(data, dtype=complex)
        
    def adjoint(self):
        return Choi(self.data.conj().T)
        
    def compose(self, other):
        d = int(np.sqrt(self.data.shape[0]))
        C1 = self.data.reshape(d, d, d, d)
        C2 = other.data.reshape(d, d, d, d)
        S1 = np.transpose(C1, (1, 3, 0, 2)).reshape(d*d, d*d)
        S2 = np.transpose(C2, (1, 3, 0, 2)).reshape(d*d, d*d)
        S12 = (S1 @ S2).reshape(d, d, d, d)
        C12 = np.transpose(S12, (2, 0, 3, 1)).reshape(d*d, d*d)
        return Choi(C12)

def initialize_adjoint_and_compose(data1, data2):
    choi1 = Choi(data1)
    choi2 = Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi

machine.finalize()
