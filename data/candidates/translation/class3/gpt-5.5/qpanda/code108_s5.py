# EVAL_META: task_id=108, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq


def initialize_adjoint_and_compose(data1, data2):
    class _Choi:
        def __init__(self, data, input_dim=None, output_dim=None):
            if isinstance(data, _Choi):
                self.data = np.array(data.data, dtype=complex, copy=True)
                self._input_dim = data._input_dim if input_dim is None else int(input_dim)
                self._output_dim = data._output_dim if output_dim is None else int(output_dim)
            else:
                arr = np.asarray(getattr(data, "data", data), dtype=complex)
                if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
                    raise ValueError("Choi data must be a square matrix.")
                self.data = np.array(arr, dtype=complex, copy=True)
                n = self.data.shape[0]
                if input_dim is None or output_dim is None:
                    root = int(round(np.sqrt(n)))
                    if root * root == n:
                        inferred_input = root
                        inferred_output = root
                    else:
                        inferred_input = 1
                        inferred_output = n
                    self._input_dim = inferred_input if input_dim is None else int(input_dim)
                    self._output_dim = inferred_output if output_dim is None else int(output_dim)
                else:
                    self._input_dim = int(input_dim)
                    self._output_dim = int(output_dim)
                if self._input_dim * self._output_dim != n:
                    raise ValueError("Input and output dimensions are incompatible with Choi data.")

        @property
        def dim(self):
            return self._input_dim, self._output_dim

        def input_dims(self):
            return (self._input_dim,)

        def output_dims(self):
            return (self._output_dim,)

        def copy(self):
            return _Choi(self)

        def to_matrix(self):
            return np.array(self.data, copy=True)

        def __array__(self, dtype=None):
            return np.asarray(self.data, dtype=dtype)

        def _to_superop(self):
            di = self._input_dim
            do = self._output_dim
            tensor = self.data.reshape((do, di, do, di), order="F")
            return tensor.transpose(0, 2, 1, 3).reshape((do * do, di * di), order="F")

        @staticmethod
        def _from_superop(superop, input_dim, output_dim):
            di = int(input_dim)
            do = int(output_dim)
            tensor = np.asarray(superop, dtype=complex).reshape((do, do, di, di), order="F")
            choi_data = tensor.transpose(0, 2, 1, 3).reshape((do * di, do * di), order="F")
            return _Choi(choi_data, input_dim=di, output_dim=do)

        def adjoint(self):
            superop = self._to_superop()
            return _Choi._from_superop(superop.conjugate().T, self._output_dim, self._input_dim)

        def compose(self, other, qargs=None, front=False):
            if qargs is not None:
                raise NotImplementedError("Subsystem composition is not supported.")
            other = other if isinstance(other, _Choi) else _Choi(other)
            self_superop = self._to_superop()
            other_superop = other._to_superop()
            if front:
                if self._input_dim != other._output_dim:
                    raise ValueError("Incompatible channel dimensions for composition.")
                composed = self_superop @ other_superop
                return _Choi._from_superop(composed, other._input_dim, self._output_dim)
            if other._input_dim != self._output_dim:
                raise ValueError("Incompatible channel dimensions for composition.")
            composed = other_superop @ self_superop
            return _Choi._from_superop(composed, self._input_dim, other._output_dim)

        def __repr__(self):
            return f"Choi({self.data!r}, input_dims={self.input_dims()}, output_dims={self.output_dims()})"

    choi1 = _Choi(data1)
    choi2 = _Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi
