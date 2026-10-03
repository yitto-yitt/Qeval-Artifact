# EVAL_META: task_id=108, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def initialize_adjoint_and_compose(data1, data2):
    class Choi:
        def __init__(self, data, input_dim=None, output_dim=None):
            if isinstance(data, Choi):
                self.data = np.array(data.data, dtype=complex, copy=True)
                self._input_dim = data._input_dim
                self._output_dim = data._output_dim
                return

            arr = np.asarray(data, dtype=complex)
            if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
                raise ValueError("Choi data must be a square matrix.")

            if input_dim is None or output_dim is None:
                dim = int(round(np.sqrt(arr.shape[0])))
                if dim * dim != arr.shape[0]:
                    raise ValueError("Cannot infer equal input and output dimensions.")
                input_dim = dim
                output_dim = dim

            if arr.shape != (input_dim * output_dim, input_dim * output_dim):
                raise ValueError("Choi data shape is incompatible with channel dimensions.")

            self.data = arr
            self._input_dim = int(input_dim)
            self._output_dim = int(output_dim)

        def __array__(self, dtype=None):
            return np.asarray(self.data, dtype=dtype)

        @property
        def shape(self):
            return self.data.shape

        def input_dims(self):
            return (self._input_dim,)

        def output_dims(self):
            return (self._output_dim,)

        def adjoint(self):
            din = self._input_dim
            dout = self._output_dim
            tensor = self.data.reshape(din, dout, din, dout)
            adj = np.conjugate(np.transpose(tensor, (1, 0, 3, 2)))
            return Choi(adj.reshape(dout * din, dout * din), input_dim=dout, output_dim=din)

        def compose(self, other):
            other = Choi(other) if not isinstance(other, Choi) else other
            if other._output_dim != self._input_dim:
                raise ValueError("Channel dimensions are incompatible for composition.")

            self_tensor = self.data.reshape(
                self._input_dim, self._output_dim, self._input_dim, self._output_dim
            )
            other_tensor = other.data.reshape(
                other._input_dim, other._output_dim, other._input_dim, other._output_dim
            )
            composed = np.einsum("mrns,rasb->manb", other_tensor, self_tensor)
            return Choi(
                composed.reshape(
                    other._input_dim * self._output_dim,
                    other._input_dim * self._output_dim,
                ),
                input_dim=other._input_dim,
                output_dim=self._output_dim,
            )

    choi1 = Choi(data1)
    choi2 = Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi
