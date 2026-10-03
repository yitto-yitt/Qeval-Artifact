# EVAL_META: task_id=108, framework=pennylane, class=3
from math import isqrt

import numpy as np
import pennylane as qml


def initialize_adjoint_and_compose(data1, data2):
    choi1 = np.array(data1, dtype=complex, copy=True)
    choi2 = np.array(data2, dtype=complex, copy=True)

    dimensions = []
    for choi in (choi1, choi2):
        if choi.ndim != 2 or choi.shape[0] != choi.shape[1]:
            raise ValueError("A Choi matrix must be square.")
        dimension = isqrt(choi.shape[0])
        if dimension == 0 or dimension * dimension != choi.shape[0]:
            raise ValueError("Cannot infer equal input and output dimensions.")
        dimensions.append(dimension)

    if dimensions[0] != dimensions[1]:
        raise ValueError("Channel dimensions are incompatible for composition.")

    dimension = dimensions[0]
    tensor1 = qml.math.reshape(choi1, (dimension,) * 4)
    tensor2 = qml.math.reshape(choi2, (dimension,) * 4)

    adjoint_choi1 = qml.math.reshape(
        qml.math.transpose(qml.math.conj(tensor1), (1, 0, 3, 2)),
        choi1.shape,
    )
    composed_choi = qml.math.reshape(
        qml.math.einsum("iajb,acbd->icjd", tensor1, tensor2),
        choi1.shape,
    )

    return choi1, adjoint_choi1, composed_choi
