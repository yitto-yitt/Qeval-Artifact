# EVAL_META: task_id=108, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq


def initialize_adjoint_and_compose(data1, data2):
    class _Choi:
        def __init__(self, data, input_dim=None, output_dim=None):
            if hasattr(data, "data"):
                arr = np.array(data.data, dtype=complex, copy=True)
                if input_dim is None and hasattr(data, "_input_dim"):
                    input_dim = data._input_dim
                if output_dim is None and hasattr(data, "_output_dim"):
                    output_dim = data._output_dim
            else:
                arr = np.array(data, dtype=complex)

            if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
                raise ValueError("Choi data must be a square matrix.")

            total = arr.shape[0]
            if input_dim is None or output_dim is None:
                dim = int(round(np.sqrt(total)))
                if dim * dim != total:
                    raise ValueError("Cannot infer input and output dimensions.")
                input_dim = dim
                output_dim = dim

            if input_dim * output_dim != total:
                raise ValueError("Input and output dimensions are incompatible with Choi data.")

            self.data = arr
            self._input_dim = int(input_dim)
            self._output_dim = int(output_dim)

        def input_dims(self):
            return (self._input_dim,)

        def output_dims(self):
            return (self._output_dim,)

        def adjoint(self):
            dout = self._output_dim
            din = self._input_dim
            adj = self.data.reshape(dout, din, dout, din).transpose(1, 0, 3, 2).conj()
            return _Choi(adj.reshape(din * dout, din * dout), input_dim=dout, output_dim=din)

        def compose(self, other):
            if not isinstance(other, _Choi):
                other = _Choi(other)

            s_self = self.data.reshape(
                self._output_dim, self._input_dim, self._output_dim, self._input_dim
            ).transpose(0, 2, 1, 3).reshape(
                self._output_dim * self._output_dim,
                self._input_dim * self._input_dim
            )

            s_other = other.data.reshape(
                other._output_dim, other._input_dim, other._output_dim, other._input_dim
            ).transpose(0, 2, 1, 3).reshape(
                other._output_dim * other._output_dim,
                other._input_dim * other._input_dim
            )

            composed_super = s_self @ s_other
            composed_choi = composed_super.reshape(
                self._output_dim, self._output_dim, other._input_dim, other._input_dim
            ).transpose(0, 2, 1, 3).reshape(
                self._output_dim * other._input_dim,
                self._output_dim * other._input_dim
            )
            return _Choi(composed_choi, input_dim=other._input_dim, output_dim=self._output_dim)

        def __array__(self, dtype=None):
            return np.asarray(self.data, dtype=dtype)

        def __repr__(self):
            return f"Choi({self.data!r})"

    choi1 = _Choi(data1)
    choi2 = _Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi
