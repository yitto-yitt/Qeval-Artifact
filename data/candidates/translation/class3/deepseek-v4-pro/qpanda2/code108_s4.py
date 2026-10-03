# EVAL_META: task_id=108, framework=qpanda2, class=3
import math
import numpy as np
from pyqpanda import *

# Global QVM and qubit allocation, kept at module scope.
machine = CPUQVM()
machine.init_qvm()
_qubits = machine.qAlloc_many(1)


class Choi:
    """Minimal Choi matrix wrapper matching Qiskit quantum_info.Choi behavior."""
    def __init__(self, data, input_dims=None, output_dims=None):
        if hasattr(data, 'data'):
            data = data.data
        self._data = np.array(data, dtype=complex)
        if self._data.ndim != 2 or self._data.shape[0] != self._data.shape[1]:
            raise ValueError("Choi matrix must be a square matrix.")
        dim = self._data.shape[0]
        d = math.isqrt(dim)
        if d * d != dim:
            if input_dims is not None and output_dims is not None:
                in_dim = input_dims if isinstance(input_dims, int) else int(np.prod(input_dims))
                out_dim = output_dims if isinstance(output_dims, int) else int(np.prod(output_dims))
                if in_dim * out_dim != dim:
                    raise ValueError("Choi matrix dimension does not match input/output dimensions.")
            else:
                raise ValueError("Choi matrix dimension must be a perfect square when dimensions are inferred automatically.")
        if input_dims is None:
            input_dims = d
        if output_dims is None:
            output_dims = d
        if isinstance(input_dims, (list, tuple)):
            input_dims = int(np.prod(input_dims))
        if isinstance(output_dims, (list, tuple)):
            output_dims = int(np.prod(output_dims))
        self._input_dim = int(input_dims)
        self._output_dim = int(output_dims)
        if self._input_dim * self._output_dim != dim:
            raise ValueError("Choi matrix dimension does not match input/output dimensions.")

    @property
    def data(self):
        return self._data

    @staticmethod
    def _choi_to_superop(data, input_dim, output_dim):
        return data.reshape(
            (output_dim, input_dim, output_dim, input_dim)
        ).transpose((0, 2, 1, 3)).reshape(
            (output_dim * output_dim, input_dim * input_dim)
        )

    @staticmethod
    def _superop_to_choi(data, input_dim, output_dim):
        return data.reshape(
            (output_dim, output_dim, input_dim, input_dim)
        ).transpose((0, 2, 1, 3)).reshape(
            (output_dim * input_dim, output_dim * input_dim)
        )

    def adjoint(self):
        superop = self._choi_to_superop(
            self._data, self._input_dim, self._output_dim
        )
        superop_adj = np.conjugate(np.transpose(superop))
        choi_adj = self._superop_to_choi(
            superop_adj, self._output_dim, self._input_dim
        )
        return Choi(
            choi_adj,
            input_dims=self._output_dim,
            output_dims=self._input_dim,
        )

    def compose(self, other, front=False):
        if hasattr(other, 'data'):
            other_data = other.data
        else:
            other_data = np.array(other, dtype=complex)

        if hasattr(other, '_input_dim'):
            other_in = other._input_dim
            other_out = other._output_dim
        else:
            other_dim = other_data.shape[0]
            other_in = other_out = math.isqrt(other_dim)
            if other_in * other_out != other_dim:
                raise ValueError("Other Choi matrix dimension must be a perfect square.")

        superop_self = self._choi_to_superop(
            self._data, self._input_dim, self._output_dim
        )
        superop_other = self._choi_to_superop(
            other_data, other_in, other_out
        )

        if front:
            if other_in != self._output_dim:
                raise ValueError("Dimension mismatch for channel composition.")
            superop_comp = superop_other @ superop_self
            in_dim = self._input_dim
            out_dim = other_out
        else:
            if self._input_dim != other_out:
                raise ValueError("Dimension mismatch for channel composition.")
            superop_comp = superop_self @ superop_other
            in_dim = other_in
            out_dim = self._output_dim

        choi_comp = self._superop_to_choi(superop_comp, in_dim, out_dim)
        return Choi(
            choi_comp,
            input_dims=in_dim,
            output_dims=out_dim,
        )


def initialize_adjoint_and_compose(data1, data2):
    choi1 = Choi(data1)
    choi2 = Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi


machine.finalize()
