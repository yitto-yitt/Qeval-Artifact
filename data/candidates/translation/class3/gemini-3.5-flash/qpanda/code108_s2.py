# EVAL_META: task_id=108, framework=qpanda, class=3
import numpy as np
import pyqpanda as pq


class Choi:

    def __init__(self, data, input_dims=None, output_dims=None):
        if isinstance(data, Choi):
            self.data = np.array(data.data, dtype=complex)
            self.input_dims = data.input_dims
            self.output_dims = data.output_dims
        else:
            self.data = np.array(data, dtype=complex)
            sz = self.data.shape[0]
            if input_dims is None or output_dims is None:
                d = int(np.sqrt(sz))
                self.input_dims = (d,)
                self.output_dims = (d,)
            else:
                self.input_dims = input_dims
                self.output_dims = output_dims

    def adjoint(self):
        d_out = np.prod(self.output_dims)
        d_in = np.prod(self.input_dims)
        J_4d = self.data.reshape(d_out, d_in, d_out, d_in)
        J_adj_4d = np.conj(J_4d.transpose(1, 0, 3, 2))
        J_adj_2d = J_adj_4d.reshape(d_in * d_out, d_in * d_out)
        return Choi(J_adj_2d, input_dims=self.output_dims, output_dims=self.input_dims)

    def compose(self, other):
        if not isinstance(other, Choi):
            other = Choi(other)
        d_C = np.prod(self.output_dims)
        d_B = np.prod(self.input_dims)
        d_A = np.prod(other.input_dims)
        J1 = self.data.reshape(d_C, d_B, d_C, d_B)
        J2 = other.data.reshape(d_B, d_A, d_B, d_A)
        J_4d = np.einsum("i j k l, j m l n -> i m k n", J1, J2)
        J_2d = J_4d.reshape(d_C * d_A, d_C * d_A)
        return Choi(J_2d, input_dims=other.input_dims, output_dims=self.output_dims)


def initialize_adjoint_and_compose(data1, data2):
    choi1 = Choi(data1)
    choi2 = Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi
