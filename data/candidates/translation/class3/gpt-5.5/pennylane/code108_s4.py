# EVAL_META: task_id=108, framework=pennylane, class=3
import pennylane as qml
import numpy as np


def initialize_adjoint_and_compose(data1, data2):
    class _ChoiArray(np.ndarray):
        def __new__(cls, data, input_dim=None, output_dim=None):
            arr = np.asarray(data, dtype=complex).view(cls)
            if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
                raise ValueError("Choi data must be a square matrix.")
            if input_dim is None or output_dim is None:
                dim = int(round(np.sqrt(arr.shape[0])))
                if dim * dim != arr.shape[0]:
                    raise ValueError("Cannot infer equal input and output dimensions.")
                input_dim = dim
                output_dim = dim
            arr._input_dim = int(input_dim)
            arr._output_dim = int(output_dim)
            return arr

        def __array_finalize__(self, obj):
            if obj is None:
                return
            self._input_dim = getattr(obj, "_input_dim", None)
            self._output_dim = getattr(obj, "_output_dim", None)

        @property
        def data(self):
            return np.asarray(self)

        def input_dims(self):
            return (self._input_dim,)

        def output_dims(self):
            return (self._output_dim,)

        def adjoint(self):
            din = self._input_dim
            dout = self._output_dim
            tensor = np.asarray(self).reshape(din, dout, din, dout)
            adj = np.conjugate(tensor).transpose(1, 0, 3, 2).reshape(dout * din, dout * din)
            return _ChoiArray(adj, input_dim=dout, output_dim=din)

        def compose(self, other, front=False):
            other = other if isinstance(other, _ChoiArray) else _ChoiArray(other)
            first, second = (other, self) if front else (self, other)

            if first._output_dim != second._input_dim:
                raise ValueError("Input/output dimensions are not compatible for composition.")

            din = first._input_dim
            dmid = first._output_dim
            dout = second._output_dim

            t_first = np.asarray(first).reshape(din, dmid, din, dmid)
            t_second = np.asarray(second).reshape(dmid, dout, dmid, dout)
            comp = np.einsum("aibj,icjd->acbd", t_first, t_second).reshape(din * dout, din * dout)
            return _ChoiArray(comp, input_dim=din, output_dim=dout)

    choi1 = _ChoiArray(data1)
    choi2 = _ChoiArray(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi
