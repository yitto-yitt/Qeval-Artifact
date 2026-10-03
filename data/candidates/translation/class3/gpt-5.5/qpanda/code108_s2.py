# EVAL_META: task_id=108, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq


def initialize_adjoint_and_compose(data1, data2):
    _ = pq

    class Choi:
        __array_priority__ = 1000

        def __init__(self, data, input_dim=None, output_dim=None):
            if isinstance(data, Choi):
                self.data = np.array(data.data, dtype=complex, copy=True)
                self._input_dim = data._input_dim if input_dim is None else int(input_dim)
                self._output_dim = data._output_dim if output_dim is None else int(output_dim)
                self.dim = (self._input_dim, self._output_dim)
                return

            arr = np.array(data, dtype=complex, copy=True)
            if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
                raise ValueError("Invalid Choi data: expected a square matrix.")

            if input_dim is None or output_dim is None:
                size = arr.shape[0]
                root = int(round(np.sqrt(size)))
                if root * root != size:
                    raise ValueError("Cannot infer equal input and output dimensions.")
                input_dim = root
                output_dim = root

            input_dim = int(input_dim)
            output_dim = int(output_dim)
            if arr.shape != (input_dim * output_dim, input_dim * output_dim):
                raise ValueError("Choi matrix shape is incompatible with channel dimensions.")

            self.data = arr
            self._input_dim = input_dim
            self._output_dim = output_dim
            self.dim = (input_dim, output_dim)

        def input_dims(self, qargs=None):
            return (self._input_dim,)

        def output_dims(self, qargs=None):
            return (self._output_dim,)

        @staticmethod
        def _choi_to_superop(mat, input_dim, output_dim):
            return np.reshape(
                np.transpose(
                    np.reshape(mat, (input_dim, output_dim, input_dim, output_dim)),
                    (3, 1, 2, 0),
                ),
                (output_dim * output_dim, input_dim * input_dim),
            )

        @staticmethod
        def _superop_to_choi(mat, input_dim, output_dim):
            return np.reshape(
                np.transpose(
                    np.reshape(mat, (output_dim, output_dim, input_dim, input_dim)),
                    (3, 1, 2, 0),
                ),
                (input_dim * output_dim, input_dim * output_dim),
            )

        def adjoint(self):
            superop = self._choi_to_superop(self.data, self._input_dim, self._output_dim)
            adj_superop = np.conjugate(superop).T
            adj_data = self._superop_to_choi(adj_superop, self._output_dim, self._input_dim)
            return Choi(adj_data, self._output_dim, self._input_dim)

        def compose(self, other):
            other = other if isinstance(other, Choi) else Choi(other)
            if self._output_dim != other._input_dim:
                raise ValueError("Channel dimensions are not compatible for composition.")

            self_superop = self._choi_to_superop(self.data, self._input_dim, self._output_dim)
            other_superop = self._choi_to_superop(other.data, other._input_dim, other._output_dim)
            composed_superop = other_superop @ self_superop
            composed_data = self._superop_to_choi(
                composed_superop, self._input_dim, other._output_dim
            )
            return Choi(composed_data, self._input_dim, other._output_dim)

        def copy(self):
            return Choi(self)

        def __array__(self, dtype=None, copy=None):
            arr = np.asarray(self.data, dtype=dtype)
            if copy:
                arr = arr.copy()
            return arr

        def __repr__(self):
            return f"Choi({repr(self.data)})"

    choi1 = Choi(data1)
    choi2 = Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi
