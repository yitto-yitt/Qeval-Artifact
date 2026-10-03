# EVAL_META: task_id=108, framework=cirq, class=3
import cirq
import numpy as np


def initialize_adjoint_and_compose(data1, data2):
    choi1 = np.asarray(data1, dtype=complex)
    choi2 = np.asarray(data2, dtype=complex)

    def _dim(choi):
        n = choi.shape[0]
        d = int(round(np.sqrt(n)))
        if d * d != n:
            raise ValueError("Choi matrix dimension must be a perfect square.")
        return d

    def _choi_to_superop(choi):
        d = _dim(choi)
        return np.transpose(choi.reshape(d, d, d, d), (1, 3, 0, 2)).reshape(d * d, d * d)

    def _superop_to_choi(superop):
        d = _dim(superop)
        return np.transpose(superop.reshape(d, d, d, d), (2, 0, 3, 1)).reshape(d * d, d * d)

    superop1 = _choi_to_superop(choi1)
    superop2 = _choi_to_superop(choi2)

    adjoint_choi1 = _superop_to_choi(superop1.conj().T)
    composed_choi = _superop_to_choi(superop1 @ superop2)

    return choi1, adjoint_choi1, composed_choi
