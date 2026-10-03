# EVAL_META: task_id=108, framework=qpanda2, class=3
import math
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_qubits = machine.qAlloc_many(1)


def initialize_adjoint_and_compose(data1, data2):
    class _Choi:
        def __init__(self, data, input_dim=None, output_dim=None):
            if isinstance(data, _Choi):
                self.data = np.array(data.data, dtype=complex, copy=True)
                self._input_dim = data._input_dim
                self._output_dim = data._output_dim
            else:
                raw = data
                if not isinstance(data, (np.ndarray, np.matrix, list, tuple)) and hasattr(data, "data"):
                    raw = data.data
                self.data = np.array(raw, dtype=complex, copy=True)
                if self.data.ndim != 2 or self.data.shape[0] != self.data.shape[1]:
                    raise ValueError("Choi data must be a square matrix.")
                if input_dim is not None and output_dim is not None:
                    self._input_dim = int(input_dim)
                    self._output_dim = int(output_dim)
                elif not isinstance(data, (np.ndarray, np.matrix, list, tuple)) and hasattr(data, "input_dims") and hasattr(data, "output_dims"):
                    in_dims = data.input_dims() if callable(data.input_dims) else data.input_dims
                    out_dims = data.output_dims() if callable(data.output_dims) else data.output_dims
                    self._input_dim = int(np.prod(in_dims))
                    self._output_dim = int(np.prod(out_dims))
                else:
                    dim = self.data.shape[0]
                    root = int(round(math.sqrt(dim)))
                    if root * root != dim:
                        raise ValueError("Cannot infer equal input and output dimensions for Choi data.")
                    self._input_dim = root
                    self._output_dim = root
            self.dim = (self._input_dim, self._output_dim)

        def input_dims(self):
            return (self._input_dim,)

        def output_dims(self):
            return (self._output_dim,)

        @staticmethod
        def _choi_to_super(mat, input_dim, output_dim):
            return np.reshape(
                np.transpose(
                    np.reshape(mat, (output_dim, input_dim, output_dim, input_dim)),
                    (0, 2, 1, 3),
                ),
                (output_dim * output_dim, input_dim * input_dim),
            )

        @staticmethod
        def _super_to_choi(mat, input_dim, output_dim):
            return np.reshape(
                np.transpose(
                    np.reshape(mat, (output_dim, output_dim, input_dim, input_dim)),
                    (0, 2, 1, 3),
                ),
                (output_dim * input_dim, output_dim * input_dim),
            )

        def adjoint(self):
            superop = self._choi_to_super(self.data, self._input_dim, self._output_dim)
            adj_superop = np.conjugate(superop.T)
            adj_data = self._super_to_choi(adj_superop, self._output_dim, self._input_dim)
            return _Choi(adj_data, input_dim=self._output_dim, output_dim=self._input_dim)

        def compose(self, other):
            other = other if isinstance(other, _Choi) else _Choi(other)
            super_self = self._choi_to_super(self.data, self._input_dim, self._output_dim)
            super_other = self._choi_to_super(other.data, other._input_dim, other._output_dim)
            composed_super = super_self @ super_other
            composed_data = self._super_to_choi(composed_super, other._input_dim, self._output_dim)
            return _Choi(composed_data, input_dim=other._input_dim, output_dim=self._output_dim)

        def copy(self):
            return _Choi(self)

        def __array__(self, dtype=None):
            return np.asarray(self.data, dtype=dtype)

        def __repr__(self):
            return f"Choi({repr(self.data)}, input_dims={self.input_dims()}, output_dims={self.output_dims()})"

    choi1 = _Choi(data1)
    choi2 = _Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi


machine.finalize()
