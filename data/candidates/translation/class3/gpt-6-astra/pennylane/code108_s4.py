# EVAL_META: task_id=108, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def initialize_adjoint_and_compose(data1, data2):
    choi1 = np.array(data1, dtype=complex, copy=True)
    choi2 = np.array(data2, dtype=complex, copy=True)

    dimensions = []
    for matrix in (choi1, choi2):
        if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
            raise ValueError("Choi matrices must be square.")
        dimension = int(np.sqrt(matrix.shape[0]))
        if dimension < 1 or dimension * dimension != matrix.shape[0]:
            raise ValueError("Cannot infer equal input and output dimensions.")
        dimensions.append(dimension)

    d1, d2 = dimensions
    if d1 != d2:
        raise ValueError("Channel dimensions are incompatible for composition.")

    tensor1 = qml.math.reshape(choi1, (d1, d1, d1, d1))
    tensor2 = qml.math.reshape(choi2, (d2, d2, d2, d2))

    adjoint_choi1 = qml.math.reshape(
        qml.math.transpose(qml.math.conj(tensor1), (1, 0, 3, 2)),
        choi1.shape,
    )
    composed_choi = qml.math.reshape(
        qml.math.einsum("iajb,acbd->icjd", tensor1, tensor2),
        choi1.shape,
    )

    return choi1, adjoint_choi1, composed_choi
