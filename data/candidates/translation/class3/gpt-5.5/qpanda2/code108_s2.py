# EVAL_META: task_id=108, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_qubits = machine.qAlloc_many(1)


def initialize_adjoint_and_compose(data1, data2):
    class Choi:
        def __init__(self, data, input_dims=None, output_dims=None):
            if isinstance(data, Choi):
                arr = np.array(data.data, dtype=complex, copy=True)
                in_dims = data.input_dims()
                out_dims = data.output_dims()
            else:
                if isinstance(data, np.ndarray) or isinstance(data, (list, tuple)):
                    arr = np.asarray(data, dtype=complex)
                elif hasattr(data, "data"):
                    arr = np.asarray(data.data, dtype=complex)
                else:
                    arr = np.asarray(data, dtype=complex)

                in_dims = None
                out_dims = None
                if hasattr(data, "input_dims") and callable(getattr(data, "input_dims")):
                    try:
                        in_dims = tuple(int(x) for x in data.input_dims())
                    except TypeError:
                        in_dims = None
                if hasattr(data, "output_dims") and callable(getattr(data, "output_dims")):
                    try:
                        out_dims = tuple(int(x) for x in data.output_dims())
                    except TypeError:
                        out_dims = None

            if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
                raise ValueError("Invalid Choi matrix data.")

            dim = int(arr.shape[0])

            def _prod(vals):
                p = 1
                for v in vals:
                    p *= int(v)
                return p

            def _default_dims(d):
                d = int(d)
                if d > 0 and (d & (d - 1)) == 0:
                    n = int(round(np.log2(d)))
                    return (2,) * n if n > 0 else (1,)
                return (d,)

            if input_dims is not None:
                in_dims = tuple(int(x) for x in input_dims)
            if output_dims is not None:
                out_dims = tuple(int(x) for x in output_dims)

            if in_dims is None or out_dims is None:
                root = int(round(np.sqrt(dim)))
                if root * root == dim:
                    if in_dims is None:
                        in_dims = _default_dims(root)
                    if out_dims is None:
                        out_dims = _default_dims(root)
                elif in_dims is None and out_dims is None:
                    in_dims = (1,)
                    out_dims = (dim,)
                elif in_dims is None:
                    out_dim = _prod(out_dims)
                    in_dims = (dim // out_dim,)
                else:
                    in_dim = _prod(in_dims)
                    out_dims = (dim // in_dim,)

            self._input_dims = tuple(in_dims)
            self._output_dims = tuple(out_dims)
            self._input_dim = _prod(self._input_dims)
            self._output_dim = _prod(self._output_dims)

            if self._input_dim * self._output_dim != dim:
                raise ValueError("Choi matrix dimensions are incompatible with data shape.")

            self.data = np.array(arr, dtype=complex, copy=True)

        @property
        def dim(self):
            return self._input_dim, self._output_dim

        @property
        def input_dim(self):
            return self._input_dim

        @property
        def output_dim(self):
            return self._output_dim

        def input_dims(self, qargs=None):
            if qargs is None:
                return self._input_dims
            return tuple(self._input_dims[i] for i in qargs)

        def output_dims(self, qargs=None):
            if qargs is None:
                return self._output_dims
            return tuple(self._output_dims[i] for i in qargs)

        def copy(self):
            return Choi(self.data, self._input_dims, self._output_dims)

        def __array__(self, dtype=None):
            return np.asarray(self.data, dtype=dtype)

        def _to_superop(self):
            din = self._input_dim
            dout = self._output_dim
            return self.data.reshape(din, dout, din, dout).transpose(1, 3, 0, 2).reshape(dout * dout, din * din)

        @staticmethod
        def _from_superop(superop, input_dims, output_dims):
            din = 1
            for v in input_dims:
                din *= int(v)
            dout = 1
            for v in output_dims:
                dout *= int(v)
            data = np.asarray(superop, dtype=complex).reshape(dout, dout, din, din).transpose(2, 0, 3, 1).reshape(din * dout, din * dout)
            return Choi(data, input_dims=input_dims, output_dims=output_dims)

        def adjoint(self):
            superop = self._to_superop().conjugate().T
            return Choi._from_superop(superop, self._output_dims, self._input_dims)

        def compose(self, other, qargs=None, front=False):
            other = Choi(other)
            if front:
                left = other
                right = self
            else:
                left = self
                right = other
            superop = left._to_superop() @ right._to_superop()
            return Choi._from_superop(superop, right.input_dims(), left.output_dims())

        def __repr__(self):
            return f"Choi({repr(self.data)})"

    choi1 = Choi(data1)
    choi2 = Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi


machine.finalize()
