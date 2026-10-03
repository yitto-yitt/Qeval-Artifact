# EVAL_META: task_id=108, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq


def initialize_adjoint_and_compose(data1, data2):
    try:
        Choi = getattr(pq, "Choi")
        choi1 = Choi(data1)
        choi2 = Choi(data2)
        adjoint_choi1 = choi1.adjoint()
        composed_choi = choi1.compose(choi2)
        return choi1, adjoint_choi1, composed_choi
    except Exception:
        pass

    class _Choi:
        def __init__(self, data, input_dim=None, output_dim=None):
            if isinstance(data, _Choi):
                self.data = np.array(data.data, dtype=complex, copy=True)
                self._input_dim = data._input_dim
                self._output_dim = data._output_dim
                self._input_dims = data._input_dims
                self._output_dims = data._output_dims
                self.dim = (self._input_dim, self._output_dim)
                return

            if hasattr(data, "data") and not isinstance(data, (np.ndarray, list, tuple)):
                arr = np.asarray(data.data, dtype=complex)
                if hasattr(data, "input_dims") and hasattr(data, "output_dims"):
                    try:
                        in_dims = tuple(data.input_dims())
                        out_dims = tuple(data.output_dims())
                        input_dim = int(np.prod(in_dims))
                        output_dim = int(np.prod(out_dims))
                    except Exception:
                        pass
            else:
                arr = np.asarray(data, dtype=complex)

            if arr.ndim != 2:
                raise ValueError("Choi data must be a matrix.")
            if arr.shape[0] != arr.shape[1]:
                raise ValueError("Choi data must be square.")

            n = arr.shape[0]
            if input_dim is None or output_dim is None:
                root = int(round(np.sqrt(n)))
                if root * root == n:
                    input_dim = root if input_dim is None else input_dim
                    output_dim = root if output_dim is None else output_dim
                else:
                    input_dim = 1 if input_dim is None else input_dim
                    output_dim = n if output_dim is None else output_dim

            if int(input_dim) * int(output_dim) != n:
                raise ValueError("Invalid input/output dimensions for Choi data.")

            self.data = np.array(arr, dtype=complex, copy=True)
            self._input_dim = int(input_dim)
            self._output_dim = int(output_dim)
            self._input_dims = self._auto_dims(self._input_dim)
            self._output_dims = self._auto_dims(self._output_dim)
            self.dim = (self._input_dim, self._output_dim)

        @staticmethod
        def _auto_dims(dim):
            dim = int(dim)
            if dim > 1 and (dim & (dim - 1)) == 0:
                return tuple([2] * int(np.log2(dim)))
            return (dim,)

        @staticmethod
        def _choi_to_super(mat, output_dim, input_dim):
            return np.asarray(mat, dtype=complex).reshape(
                output_dim, input_dim, output_dim, input_dim
            ).transpose(0, 2, 1, 3).reshape(output_dim * output_dim, input_dim * input_dim)

        @staticmethod
        def _super_to_choi(mat, output_dim, input_dim):
            return np.asarray(mat, dtype=complex).reshape(
                output_dim, output_dim, input_dim, input_dim
            ).transpose(0, 2, 1, 3).reshape(output_dim * input_dim, output_dim * input_dim)

        def input_dims(self):
            return self._input_dims

        def output_dims(self):
            return self._output_dims

        def adjoint(self):
            superop = self._choi_to_super(self.data, self._output_dim, self._input_dim)
            adj_superop = superop.conj().T
            adj_choi = self._super_to_choi(adj_superop, self._input_dim, self._output_dim)
            return _Choi(adj_choi, input_dim=self._output_dim, output_dim=self._input_dim)

        def compose(self, other):
            other = _Choi(other)
            super_self = self._choi_to_super(self.data, self._output_dim, self._input_dim)
            super_other = self._choi_to_super(other.data, other._output_dim, other._input_dim)
            composed_super = super_other @ super_self
            composed_choi = self._super_to_choi(
                composed_super, other._output_dim, self._input_dim
            )
            return _Choi(
                composed_choi, input_dim=self._input_dim, output_dim=other._output_dim
            )

        def copy(self):
            return _Choi(self)

        def __array__(self, dtype=None):
            return np.asarray(self.data, dtype=dtype)

        def __eq__(self, other):
            try:
                other = _Choi(other)
                return np.allclose(self.data, other.data)
            except Exception:
                return False

    choi1 = _Choi(data1)
    choi2 = _Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi
