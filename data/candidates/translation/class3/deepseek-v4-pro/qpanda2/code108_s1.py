# EVAL_META: task_id=108, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)


def initialize_adjoint_and_compose(data1, data2):
    class Choi:
        def __init__(self, data):
            if isinstance(data, np.ndarray):
                arr = data
            else:
                arr = getattr(data, 'data', data)
            arr = np.asarray(arr, dtype=complex)
            if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
                raise ValueError("Choi matrix must be square")
            dim = int(np.sqrt(arr.shape[0]))
            if dim * dim != arr.shape[0]:
                raise ValueError("Choi matrix dimension must be a perfect square")
            self._data = arr.copy()
            self._dim = dim

        @property
        def data(self):
            return self._data

        def __array__(self, dtype=None):
            if dtype is not None:
                return self._data.astype(dtype)
            return self._data

        def adjoint(self):
            return type(self)(self._data.T)

        def _to_superop(self):
            d = self._dim
            J_4d = self._data.reshape(d, d, d, d)
            S_4d = np.transpose(J_4d, (1, 3, 0, 2))
            return S_4d.reshape(d * d, d * d, order='F')

        @classmethod
        def _from_superop(cls, S, dim):
            S_4d = S.reshape(dim, dim, dim, dim, order='F')
            J_4d = np.transpose(S_4d, (2, 0, 3, 1))
            J = J_4d.reshape(dim * dim, dim * dim)
            return cls(J)

        def compose(self, other):
            other_choi = type(self)(other)
            S1 = self._to_superop()
            S2 = other_choi._to_superop()
            S_composed = S1 @ S2
            return type(self)._from_superop(S_composed, self._dim)

    choi1 = Choi(data1)
    choi2 = Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi


machine.finalize()
