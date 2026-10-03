# EVAL_META: task_id=108, framework=pennylane, class=3
import numpy as np


def initialize_adjoint_and_compose(data1, data2):
    choi1 = np.asarray(data1, dtype=complex)
    choi2 = np.asarray(data2, dtype=complex)

    adjoint_choi1 = np.conjugate(choi1.T)

    dim = int(np.sqrt(choi1.shape[0]))

    def _choi_to_superop(choi):
        return np.reshape(
            np.transpose(np.reshape(choi, (dim, dim, dim, dim)), (1, 3, 0, 2)),
            (dim * dim, dim * dim),
        )

    def _superop_to_choi(sop):
        return np.reshape(
            np.transpose(np.reshape(sop, (dim, dim, dim, dim)), (2, 0, 3, 1)),
            (dim * dim, dim * dim),
        )

    superop1 = _choi_to_superop(choi1)
    superop2 = _choi_to_superop(choi2)
    composed_superop = superop1 @ superop2
    composed_choi = _superop_to_choi(composed_superop)

    return choi1, adjoint_choi1, composed_choi
