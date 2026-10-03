# EVAL_META: task_id=108, framework=pennylane, class=3
import pennylane as qml
import numpy as np

class Choi:
    def __init__(self, data):
        if isinstance(data, Choi):
            self.data = np.array(data.data)
        elif hasattr(data, 'data'):
            self.data = np.array(data.data)
        else:
            self.data = np.array(data)
        
        total_dim = self.data.shape[0]
        self.dim = int(np.sqrt(total_dim))

    def adjoint(self):
        d = self.dim
        tensor = self.data.reshape(d, d, d, d)
        tensor_conj = np.conj(tensor)
        adj_tensor = np.transpose(tensor_conj, (1, 0, 3, 2))
        adj_data = adj_tensor.reshape(d*d, d*d)
        return Choi(adj_data)

    def compose(self, other):
        if not isinstance(other, Choi):
            other = Choi(other)
        d1 = other.dim
        d2 = self.dim
        
        B_tensor = other.data.reshape(d1, d1, d1, d1)
        A_tensor = self.data.reshape(d2, d2, d2, d2)
        
        out_tensor = np.einsum('ikjl,kulv->iujv', B_tensor, A_tensor)
        out_data = out_tensor.reshape(d1*d2, d1*d2)
        return Choi(out_data)


def initialize_adjoint_and_compose(data1, data2):
    choi1 = Choi(data1)
    choi2 = Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi
