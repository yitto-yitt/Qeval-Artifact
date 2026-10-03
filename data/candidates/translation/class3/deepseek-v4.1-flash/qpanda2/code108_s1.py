# EVAL_META: task_id=108, framework=qpanda2, class=3
import numpy as np
from pyqpanda import CPUQVM, qAlloc_many

# Global QVM initialization
machine = CPUQVM()
machine.init_qvm()
qubits = qAlloc_many(2)

class Choi:
    def __init__(self, data):
        if isinstance(data, Choi):
            self._data = data._data
            self._input_dims = data._input_dims
            self._output_dims = data._output_dims
        elif isinstance(data, np.ndarray):
            self._data = np.array(data, dtype=complex)
            d = int(np.sqrt(self._data.shape[0]))
            if d * d != self._data.shape[0]:
                raise ValueError("Invalid Choi matrix shape")
            self._input_dims = [d]
            self._output_dims = [d]
        else:
            raise TypeError("Unsupported data type for Choi")

    def adjoint(self):
        d_out = self._output_dims[0]
        d_in = self._input_dims[0]
        mat = self._data.reshape(d_out, d_in, d_out, d_in)
        mat_adj = np.conj(mat.transpose(1, 0, 3, 2))
        J_adj = mat_adj.reshape(d_in * d_out, d_in * d_out)
        new_choi = Choi(J_adj)
        new_choi._input_dims = self._output_dims
        new_choi._output_dims = self._input_dims
        return new_choi

    def compose(self, other):
        def choi_to_transfer(choi):
            d_out = choi._output_dims[0]
            d_in = choi._input_dims[0]
            J = choi._data.reshape(d_out, d_in, d_out, d_in)
            T = J.transpose(0, 2, 1, 3).reshape(d_out * d_out, d_in * d_in)
            return T

        def transfer_to_choi(T, d_out, d_in):
            T = T.reshape(d_out, d_out, d_in, d_in)
            J = T.transpose(0, 2, 1, 3).reshape(d_out * d_in, d_out * d_in)
            new_choi = Choi(J)
            new_choi._output_dims = [d_out]
            new_choi._input_dims = [d_in]
            return new_choi

        d_out1 = self._output_dims[0]
        d_in1 = self._input_dims[0]
        d_out2 = other._output_dims[0]
        d_in2 = other._input_dims[0]
        if d_out2 != d_in1:
            raise ValueError("Incompatible dimensions for composition")
        T1 = choi_to_transfer(self)
        T2 = choi_to_transfer(other)
        T_composed = T1 @ T2
        return transfer_to_choi(T_composed, d_out1, d_in2)


def initialize_adjoint_and_compose(data1, data2):
    choi1 = Choi(data1)
    choi2 = Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi


machine.finalize()
