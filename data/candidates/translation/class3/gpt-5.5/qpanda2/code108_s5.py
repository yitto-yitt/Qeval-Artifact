# EVAL_META: task_id=108, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_qubits = machine.qAlloc_many(1)


def initialize_adjoint_and_compose(data1, data2):
    class _Choi:
        def __init__(self, data, input_dims=None, output_dims=None):
            if isinstance(data, _Choi):
                raw = data.data
                if input_dims is None:
                    input_dims = data.input_dims()
                if output_dims is None:
                    output_dims = data.output_dims()
            elif hasattr(data, "data") and not isinstance(data, (np.ndarray, np.matrix)):
                raw = data.data
                if input_dims is None and hasattr(data, "input_dims"):
                    attr = data.input_dims
                    input_dims = attr() if callable(attr) else attr
                if output_dims is None and hasattr(data, "output_dims"):
                    attr = data.output_dims
                    output_dims = attr() if callable(attr) else attr
            else:
                raw = data

            arr = np.asarray(raw, dtype=complex)
            if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
                raise ValueError("Input data must be a square matrix.")

            total_dim = arr.shape[0]

            if input_dims is not None:
                input_dims = self._as_tuple(input_dims)
            if output_dims is not None:
                output_dims = self._as_tuple(output_dims)

            if input_dims is None and output_dims is None:
                root = int(round(np.sqrt(total_dim)))
                if root * root != total_dim:
                    raise ValueError("Cannot infer equal input and output dimensions.")
                input_dims = (root,)
                output_dims = (root,)
            elif input_dims is None:
                out_dim = int(np.prod(output_dims))
                if total_dim % out_dim != 0:
                    raise ValueError("Invalid output dimensions.")
                input_dims = (total_dim // out_dim,)
            elif output_dims is None:
                in_dim = int(np.prod(input_dims))
                if total_dim % in_dim != 0:
                    raise ValueError("Invalid input dimensions.")
                output_dims = (total_dim // in_dim,)

            self._input_dims = tuple(int(x) for x in input_dims)
            self._output_dims = tuple(int(x) for x in output_dims)
            self._input_dim = int(np.prod(self._input_dims))
            self._output_dim = int(np.prod(self._output_dims))

            if self._input_dim * self._output_dim != total_dim:
                raise ValueError("Input/output dimensions do not match matrix size.")

            self.data = np.array(arr, dtype=complex, copy=True)
            self.dim = (self._input_dim, self._output_dim)

        @staticmethod
        def _as_tuple(dims):
            if isinstance(dims, int):
                return (dims,)
            return tuple(dims)

        @staticmethod
        def _super_to_choi(super_data, input_dim, output_dim):
            return np.asarray(super_data, dtype=complex).reshape(
                (output_dim, output_dim, input_dim, input_dim)
            ).transpose(2, 0, 3, 1).reshape(
                (input_dim * output_dim, input_dim * output_dim)
            )

        def _to_super(self):
            return self.data.reshape(
                (self._input_dim, self._output_dim, self._input_dim, self._output_dim)
            ).transpose(1, 3, 0, 2).reshape(
                (self._output_dim * self._output_dim, self._input_dim * self._input_dim)
            )

        def input_dims(self, qargs=None):
            if qargs is None:
                return self._input_dims
            return tuple(self._input_dims[i] for i in qargs)

        def output_dims(self, qargs=None):
            if qargs is None:
                return self._output_dims
            return tuple(self._output_dims[i] for i in qargs)

        def adjoint(self):
            super_adjoint = self._to_super().conjugate().transpose()
            choi_data = self._super_to_choi(
                super_adjoint, self._output_dim, self._input_dim
            )
            return _Choi(
                choi_data,
                input_dims=self._output_dims,
                output_dims=self._input_dims,
            )

        def compose(self, other, qargs=None, front=False):
            if qargs is not None:
                raise NotImplementedError("Subsystem composition is not implemented.")
            other = _Choi(other)
            if front:
                return other.compose(self)
            if self._input_dim != other._output_dim:
                raise ValueError("Channel dimensions are not compatible for composition.")
            composed_super = self._to_super() @ other._to_super()
            choi_data = self._super_to_choi(
                composed_super, other._input_dim, self._output_dim
            )
            return _Choi(
                choi_data,
                input_dims=other.input_dims(),
                output_dims=self.output_dims(),
            )

        def copy(self):
            return _Choi(
                self.data.copy(),
                input_dims=self._input_dims,
                output_dims=self._output_dims,
            )

        def __array__(self, dtype=None):
            return np.asarray(self.data, dtype=dtype) if dtype is not None else self.data

        def __eq__(self, other):
            other = _Choi(other)
            return (
                self.input_dims() == other.input_dims()
                and self.output_dims() == other.output_dims()
                and np.allclose(self.data, other.data)
            )

    choi1 = _Choi(data1)
    choi2 = _Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi


machine.finalize()
