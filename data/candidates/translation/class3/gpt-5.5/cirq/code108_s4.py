# EVAL_META: task_id=108, framework=cirq, class=3
import cirq
import numpy as np


def initialize_adjoint_and_compose(data1, data2):
    def _as_matrix(data):
        if hasattr(data, "data") and not isinstance(data, np.ndarray):
            try:
                arr = np.asarray(data.data, dtype=complex)
                if arr.ndim == 2:
                    return np.array(arr, dtype=complex, copy=True)
            except Exception:
                pass
        return np.array(data, dtype=complex, copy=True)

    def _infer_dims(mat):
        if mat.ndim != 2 or mat.shape[0] != mat.shape[1]:
            raise ValueError("Choi data must be a square matrix.")
        dim = mat.shape[0]
        base_dim = int(round(np.sqrt(dim)))
        if base_dim * base_dim != dim:
            raise ValueError("Cannot infer equal input and output dimensions from Choi data.")
        return base_dim, base_dim

    def _choi_to_superop(choi, input_dim, output_dim):
        return np.reshape(
            np.transpose(
                np.reshape(choi, (input_dim, output_dim, input_dim, output_dim)),
                (3, 1, 2, 0),
            ),
            (output_dim * output_dim, input_dim * input_dim),
        )

    def _superop_to_choi(superop, input_dim, output_dim):
        return np.reshape(
            np.transpose(
                np.reshape(superop, (output_dim, output_dim, input_dim, input_dim)),
                (3, 1, 2, 0),
            ),
            (input_dim * output_dim, input_dim * output_dim),
        )

    class _ChoiMatrix(np.ndarray):
        __array_priority__ = 1000

        def __new__(cls, data, input_dim=None, output_dim=None):
            arr = _as_matrix(data)
            if input_dim is None or output_dim is None:
                input_dim, output_dim = _infer_dims(arr)
            obj = arr.view(cls)
            obj.input_dim = int(input_dim)
            obj.output_dim = int(output_dim)
            return obj

        def __array_finalize__(self, obj):
            if obj is None:
                return
            self.input_dim = getattr(obj, "input_dim", None)
            self.output_dim = getattr(obj, "output_dim", None)

        @property
        def data(self):
            return self.view(np.ndarray)

        def input_dims(self):
            return (self.input_dim,)

        def output_dims(self):
            return (self.output_dim,)

        def adjoint(self):
            superop = _choi_to_superop(self.view(np.ndarray), self.input_dim, self.output_dim)
            adjoint_superop = np.conjugate(superop).T
            return _ChoiMatrix(
                _superop_to_choi(adjoint_superop, self.output_dim, self.input_dim),
                input_dim=self.output_dim,
                output_dim=self.input_dim,
            )

        def compose(self, other, front=False):
            other = other if isinstance(other, _ChoiMatrix) else _ChoiMatrix(other)
            self_superop = _choi_to_superop(self.view(np.ndarray), self.input_dim, self.output_dim)
            other_superop = _choi_to_superop(other.view(np.ndarray), other.input_dim, other.output_dim)
            if front:
                composed_superop = other_superop @ self_superop
                input_dim = self.input_dim
                output_dim = other.output_dim
            else:
                composed_superop = self_superop @ other_superop
                input_dim = other.input_dim
                output_dim = self.output_dim
            return _ChoiMatrix(
                _superop_to_choi(composed_superop, input_dim, output_dim),
                input_dim=input_dim,
                output_dim=output_dim,
            )

    choi1 = _ChoiMatrix(data1)
    choi2 = _ChoiMatrix(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi
