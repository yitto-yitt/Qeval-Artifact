# EVAL_META: task_id=108, framework=cirq, class=3
import numpy as np
import cirq


def initialize_adjoint_and_compose(data1, data2):
    choi1 = np.asarray(data1, dtype=complex)
    choi2 = np.asarray(data2, dtype=complex)

    dim1 = int(round(np.sqrt(choi1.shape[0])))
    dim2 = int(round(np.sqrt(choi2.shape[0])))

    adjoint_choi1 = np.conjugate(
        choi1.reshape(dim1, dim1, dim1, dim1).transpose(1, 0, 3, 2)
    ).reshape(choi1.shape)

    superop1 = choi1.reshape(dim1, dim1, dim1, dim1).transpose(1, 3, 0, 2).reshape(
        dim1 * dim1, dim1 * dim1
    )
    superop2 = choi2.reshape(dim2, dim2, dim2, dim2).transpose(1, 3, 0, 2).reshape(
        dim2 * dim2, dim2 * dim2
    )

    composed_superop = superop2 @ superop1
    composed_choi = composed_superop.reshape(dim1, dim1, dim1, dim1).transpose(
        2, 0, 3, 1
    ).reshape(choi1.shape)

    return choi1, adjoint_choi1, composed_choi
