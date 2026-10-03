# EVAL_META: task_id=108, framework=qpanda2, class=3
import numpy as np
from pyqpanda import *

# Global QVM initialization
machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(4)


class Choi:

    def __init__(self, data):
        if isinstance(data, Choi):
            self.data = np.array(data.data, dtype=complex)
            return

        if hasattr(data, "to_operator"):
            data = data.to_operator()
        if hasattr(data, "data"):
            data = data.data

        mat = np.array(data, dtype=complex)
        N = mat.shape[0]

        is_unitary = False
        if mat.ndim == 2 and mat.shape[0] == mat.shape[1]:
            identity = np.eye(N)
            if np.allclose(mat @ mat.conj().T, identity, atol=1e-5):
                is_unitary = True

        if is_unitary:
            vec_U = mat.flatten(order="F")
            self.data = np.outer(vec_U, vec_U.conj())
        else:
            self.data = mat

    def adjoint(self):
        d2 = self.data.shape[0]
        d = int(np.round(np.sqrt(d2)))
        J_conj = self.data.conj()
        J_adj = (
            J_conj.reshape(d, d, d, d)
            .transpose(1, 0, 3, 2)
            .reshape(d2, d2)
        )
        return Choi(J_adj)

    def compose(self, other):
        if not isinstance(other, Choi):
            other = Choi(other)
        d2 = self.data.shape[0]
        d = int(np.round(np.sqrt(d2)))

        K1 = (
            self.data.reshape(d, d, d, d)
            .transpose(1, 3, 0, 2)
            .reshape(d2, d2)
        )
        K2 = (
            other.data.reshape(d, d, d, d)
            .transpose(1, 3, 0, 2)
            .reshape(d2, d2)
        )

        K_composed = K1 @ K2

        J_composed = (
            K_composed.reshape(d, d, d, d)
            .transpose(2, 0, 3, 1)
            .reshape(d2, d2)
        )
        return Choi(J_composed)


def initialize_adjoint_and_compose(data1, data2):
    choi1 = Choi(data1)
    choi2 = Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi


machine.finalize()
