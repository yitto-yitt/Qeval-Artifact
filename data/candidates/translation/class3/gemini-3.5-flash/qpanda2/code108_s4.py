# EVAL_META: task_id=108, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

# Global QVM initialization
machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(4)


class Choi:

    def __init__(self, data):
        if isinstance(data, Choi):
            self.data = np.array(data.data, copy=True)
        else:
            self.data = np.array(data, dtype=complex)

    def adjoint(self):
        d = int(np.sqrt(self.data.shape[0]))
        S = (
            self.data.reshape((d, d, d, d))
            .transpose(0, 2, 1, 3)
            .reshape((d * d, d * d))
        )
        S_adj = S.conj().T
        J_adj = (
            S_adj.reshape((d, d, d, d))
            .transpose(0, 2, 1, 3)
            .reshape((d * d, d * d))
        )
        return Choi(J_adj)

    def compose(self, other):
        if not isinstance(other, Choi):
            other = Choi(other)
        d = int(np.sqrt(self.data.shape[0]))
        S1 = (
            self.data.reshape((d, d, d, d))
            .transpose(0, 2, 1, 3)
            .reshape((d * d, d * d))
        )
        S2 = (
            other.data.reshape((d, d, d, d))
            .transpose(0, 2, 1, 3)
            .reshape((d * d, d * d))
        )
        S_composed = S2 @ S1
        J_composed = (
            S_composed.reshape((d, d, d, d))
            .transpose(0, 2, 1, 3)
            .reshape((d * d, d * d))
        )
        return Choi(J_composed)


def initialize_adjoint_and_compose(data1, data2):
    choi1 = Choi(data1)
    choi2 = Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi


# Manual Cleanup
machine.finalize()
