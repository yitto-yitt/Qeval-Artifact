# EVAL_META: task_id=108, framework=cirq, class=3
import numpy as np
import cirq


def initialize_adjoint_and_compose(data1, data2):
    def _to_choi_array(data):
        if isinstance(data, np.ndarray):
            arr = np.array(data, dtype=complex, copy=True)
        else:
            try:
                arr = np.array(data, dtype=complex, copy=True)
            except Exception:
                if cirq.has_kraus(data):
                    arr = np.array(cirq.kraus_to_choi(cirq.kraus(data)), dtype=complex, copy=True)
                else:
                    raise
        if arr.ndim == 3 and arr.shape[1] == arr.shape[2]:
            arr = np.array(cirq.kraus_to_choi([arr[i] for i in range(arr.shape[0])]), dtype=complex)
        if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
            raise ValueError("Choi data must be a square matrix.")
        return arr

    def _dims_from_matrix(mat):
        size = mat.shape[0]
        dim = int(round(np.sqrt(size)))
        if dim * dim != size:
            raise ValueError("Cannot infer equal input and output dimensions from Choi matrix shape.")
        return dim, dim

    def _adjoint_choi(mat, input_dim, output_dim):
        tensor = mat.reshape(input_dim, output_dim, input_dim, output_dim)
        return np.conjugate(np.transpose(tensor, (1, 0, 3, 2))).reshape(
            output_dim * input_dim, output_dim * input_dim
        )

    def _compose_choi(mat1, in1, out1, mat2, in2, out2):
        if in1 != out2:
            raise ValueError("Incompatible Choi dimensions for composition.")
        tensor1 = mat1.reshape(in1, out1, in1, out1)
        tensor2 = mat2.reshape(in2, out2, in2, out2)
        composed = np.einsum("iajb,acbd->icjd", tensor2, tensor1)
        return composed.reshape(in2 * out1, in2 * out1)

    class _ChoiMatrix(np.ndarray):
        def __new__(cls, data, input_dim=None, output_dim=None):
            obj = np.asarray(data, dtype=complex).view(cls)
            obj._input_dim = input_dim
            obj._output_dim = output_dim
            return obj

        def __array_finalize__(self, obj):
            if obj is None:
                return
            self._input_dim = getattr(obj, "_input_dim", None)
            self._output_dim = getattr(obj, "_output_dim", None)

        @property
        def data(self):
            return self.view(np.ndarray)

        def adjoint(self):
            return _ChoiMatrix(
                _adjoint_choi(self.view(np.ndarray), self._input_dim, self._output_dim),
                self._output_dim,
                self._input_dim,
            )

        def compose(self, other):
            return _ChoiMatrix(
                _compose_choi(
                    self.view(np.ndarray),
                    self._input_dim,
                    self._output_dim,
                    np.asarray(other, dtype=complex),
                    other._input_dim,
                    other._output_dim,
                ),
                other._input_dim,
                self._output_dim,
            )

    arr1 = _to_choi_array(data1)
    arr2 = _to_choi_array(data2)
    in1, out1 = _dims_from_matrix(arr1)
    in2, out2 = _dims_from_matrix(arr2)

    choi1 = _ChoiMatrix(arr1, in1, out1)
    choi2 = _ChoiMatrix(arr2, in2, out2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi
