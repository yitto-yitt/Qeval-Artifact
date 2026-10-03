# EVAL_META: task_id=108, framework=cirq, class=3
import numpy as np
import cirq

class Choi:
    def __init__(self, data):
        data = np.asarray(data, dtype=complex)
        if data.ndim == 3:
            self.data = cirq.kraus_to_choi(list(data))
        elif data.ndim == 2:
            d = data.shape[0]
            if d > 0 and np.allclose(data @ data.conj().T, np.eye(d), atol=1e-6):
                self.data = cirq.kraus_to_choi([data])
            else:
                self.data = data
        else:
            self.data = data

    def adjoint(self):
        adj = Choi.__new__(Choi)
        adj.data = self.data.conj().T
        return adj

    def compose(self, other):
        kraus1 = cirq.choi_to_kraus(self.data, atol=1e-6)
        kraus2 = cirq.choi_to_kraus(other.data, atol=1e-6)
        kraus_composed = [k2 @ k1 for k1 in kraus1 for k2 in kraus2]
        comp = Choi.__new__(Choi)
        comp.data = cirq.kraus_to_choi(kraus_composed)
        return comp

    def __array__(self):
        return self.data

def initialize_adjoint_and_compose(data1, data2):
    choi1 = Choi(data1)
    choi2 = Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi
