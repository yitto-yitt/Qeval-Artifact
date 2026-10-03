# EVAL_META: task_id=108, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as qp


class Choi:

    def __init__(self, data, input_dims=None, output_dims=None):
        if isinstance(data, Choi):
            self.data = np.array(data.data, dtype=complex)
            self._input_dims = data._input_dims
            self._output_dims = data._output_dims
        else:
            self.data = np.array(data, dtype=complex)
            dim = self.data.shape[0]
            if input_dims is None or output_dims is None:
                side = int(np.sqrt(dim))
                self._input_dims = (side,)
                self._output_dims = (side,)
            else:
                self._input_dims = input_dims
                self._output_dims = output_dims

    def __array__(self, dtype=None):
        if dtype:
            return self.data.astype(dtype)
        return self.data

    @property
    def input_dims(self):
        return self._input_dims

    @property
    def output_dims(self):
        return self._output_dims

    def adjoint(self):
        d1 = np.prod(self._input_dims)
        d2 = np.prod(self._output_dims)
        reshaped = self.data.reshape(d1, d2, d1, d2)
        transposed = np.transpose(reshaped, (3, 2, 1, 0))
        adj_data = transposed.reshape(d2 * d1, d2 * d1)
        return Choi(
            adj_data, input_dims=self._output_dims, output_dims=self._input_dims
        )

    def compose(self, other, front=False):
        if not isinstance(other, Choi):
            other = Choi(other)

        if front:
            first, second = self, other
        else:
            first, second = other, self

        d_in1 = np.prod(first.input_dims)
        d_out1 = np.prod(first.output_dims)
        d_in2 = np.prod(second.input_dims)
        d_out2 = np.prod(second.output_dims)

        S1 = (
            np.transpose(first.data.reshape(d_in1, d_out1, d_in1, d_out1), (1, 3, 0, 2))
            .reshape(d_out1**2, d_in1**2)
        )
        S2 = (
            np.transpose(
                second.data.reshape(d_in2, d_out2, d_in2, d_out2), (1, 3, 0, 2)
            )
            .reshape(d_out2**2, d_in2**2)
        )

        S_comp = S2 @ S1

        reshaped = S_comp.reshape(d_out2, d_out2, d_in1, d_in1)
        transposed = np.transpose(reshaped, (2, 0, 3, 1))
        comp_data = transposed.reshape(d_in1 * d_out2, d_in1 * d_out2)

        return Choi(
            comp_data, input_dims=first.input_dims, output_dims=second.output_dims
        )


def initialize_adjoint_and_compose(data1, data2):
    choi1 = Choi(data1)
    choi2 = Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi
