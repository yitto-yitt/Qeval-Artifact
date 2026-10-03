# EVAL_META: task_id=108, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(1)
c = machine.cAlloc_many(1)


def initialize_adjoint_and_compose(data1, data2):
    class Choi:
        def __init__(self, data, input_dims=None, output_dims=None):
            if hasattr(data, "data"):
                arr = np.array(data.data, dtype=complex, copy=True)
                if input_dims is None and hasattr(data, "input_dims"):
                    input_dims = data.input_dims()
                if output_dims is None and hasattr(data, "output_dims"):
                    output_dims = data.output_dims()
            else:
                arr = np.array(data, dtype=complex, copy=True)

            if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
                raise ValueError("Choi data must be a square matrix")

            total_dim = arr.shape[0]
            if input_dims is None and output_dims is None:
                channel_dim = int(round(np.sqrt(total_dim)))
                if channel_dim * channel_dim != total_dim:
                    raise ValueError("Cannot infer Choi input and output dimensions")
                input_dims = self._factor_dims(channel_dim)
                output_dims = self._factor_dims(channel_dim)
            elif input_dims is None:
                output_dim = int(np.prod(output_dims))
                if total_dim % output_dim != 0:
                    raise ValueError("Invalid output dimensions for Choi data")
                input_dims = self._factor_dims(total_dim // output_dim)
            elif output_dims is None:
                input_dim = int(np.prod(input_dims))
                if total_dim % input_dim != 0:
                    raise ValueError("Invalid input dimensions for Choi data")
                output_dims = self._factor_dims(total_dim // input_dim)

            self.data = arr
            self._input_dims = tuple(input_dims)
            self._output_dims = tuple(output_dims)

        @staticmethod
        def _factor_dims(dim):
            dim = int(dim)
            if dim > 0:
                n = int(round(np.log2(dim)))
                if 2 ** n == dim:
                    return (2,) * n
            return (dim,)

        @property
        def dim(self):
            return int(np.prod(self._input_dims)), int(np.prod(self._output_dims))

        def input_dims(self):
            return self._input_dims

        def output_dims(self):
            return self._output_dims

        def copy(self):
            return Choi(self.data.copy(), self._input_dims, self._output_dims)

        def __array__(self, dtype=None):
            return np.asarray(self.data, dtype=dtype)

        def _to_superop(self):
            input_dim, output_dim = self.dim
            return (
                self.data.reshape(input_dim, output_dim, input_dim, output_dim)
                .transpose(1, 3, 0, 2)
                .reshape(output_dim * output_dim, input_dim * input_dim)
            )

        @staticmethod
        def _from_superop(superop, input_dims, output_dims):
            input_dim = int(np.prod(input_dims))
            output_dim = int(np.prod(output_dims))
            choi_data = (
                np.asarray(superop, dtype=complex)
                .reshape(output_dim, output_dim, input_dim, input_dim)
                .transpose(2, 0, 3, 1)
                .reshape(input_dim * output_dim, input_dim * output_dim)
            )
            return Choi(choi_data, input_dims, output_dims)

        def adjoint(self):
            input_dim, output_dim = self.dim
            adjoint_data = (
                self.data.reshape(input_dim, output_dim, input_dim, output_dim)
                .transpose(1, 0, 3, 2)
                .conj()
                .reshape(input_dim * output_dim, input_dim * output_dim)
            )
            return Choi(adjoint_data, self._output_dims, self._input_dims)

        def compose(self, other, qargs=None, front=False):
            if qargs is not None:
                raise NotImplementedError("qargs composition is not supported")
            other = Choi(other)
            self_input_dim, self_output_dim = self.dim
            other_input_dim, other_output_dim = other.dim
            self_super = self._to_superop()
            other_super = other._to_superop()

            if front:
                if other_output_dim != self_input_dim:
                    raise ValueError("Channel dimensions are not compatible for composition")
                composed = self_super @ other_super
                return Choi._from_superop(composed, other.input_dims(), self.output_dims())

            if self_output_dim != other_input_dim:
                raise ValueError("Channel dimensions are not compatible for composition")
            composed = other_super @ self_super
            return Choi._from_superop(composed, self.input_dims(), other.output_dims())

    choi1 = Choi(data1)
    choi2 = Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi


machine.finalize()
