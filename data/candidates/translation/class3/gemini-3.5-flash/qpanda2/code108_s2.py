# EVAL_META: task_id=108, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np
import atexit

# Initialize global QVM
machine = pq.CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(4)

class Choi:
    def __init__(self, data, input_dim=None, output_dim=None):
        if isinstance(data, Choi):
            self.data = np.array(data.data)
            self._input_dim = data._input_dim
            self._output_dim = data._output_dim
        elif isinstance(data, (pq.QProg, pq.QCircuit)):
            prog = pq.QProg()
            prog << data
            u_list = machine.get_unitary(prog)
            dim = int(np.sqrt(len(u_list)))
            U = np.array(u_list).reshape(dim, dim)
            V = U.T.flatten()
            self.data = np.outer(V, V.conj())
            self._input_dim = dim
            self._output_dim = dim
        else:
            self.data = np.array(data)
            if input_dim is not None and output_dim is not None:
                self._input_dim = input_dim
                self._output_dim = output_dim
            else:
                dim = int(np.sqrt(self.data.shape[0]))
                self._input_dim = dim
                self._output_dim = dim

    def to_superop(self):
        d_in = self._input_dim
        d_out = self._output_dim
        J = self.data.reshape(d_in, d_out, d_in, d_out)
        S = J.transpose(1, 3, 0, 2).reshape(d_out**2, d_in**2)
        return S

    @classmethod
    def from_superop(cls, S, input_dim, output_dim):
        S_tensor = S.reshape(output_dim, output_dim, input_dim, input_dim)
        J = S_tensor.transpose(2, 0, 3, 1).reshape(input_dim * output_dim, input_dim * output_dim)
        return cls(J, input_dim, output_dim)

    def adjoint(self):
        d_in = self._input_dim
        d_out = self._output_dim
        J_tensor = self.data.reshape(d_in, d_out, d_in, d_out)
        J_adj = J_tensor.conj().transpose(1, 0, 3, 2).reshape(d_out * d_in, d_out * d_in)
        return Choi(J_adj, input_dim=d_out, output_dim=d_in)

    def compose(self, other):
        if not isinstance(other, Choi):
            other = Choi(other)
        S1 = self.to_superop()
        S2 = other.to_superop()
        S_composed = S2 @ S1
        return Choi.from_superop(S_composed, self._input_dim, other._output_dim)

def initialize_adjoint_and_compose(data1, data2):
    choi1 = Choi(data1)
    choi2 = Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi

atexit.register(machine.finalize)
