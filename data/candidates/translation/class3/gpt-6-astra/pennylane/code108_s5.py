# EVAL_META: task_id=108, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def initialize_adjoint_and_compose(data1, data2):
    choi1 = np.array(data1, dtype=complex, copy=True)
    choi2 = np.array(data2, dtype=complex, copy=True)

    dimensions = []
    for choi in (choi1, choi2):
        if choi.ndim != 2 or choi.shape[0] != choi.shape[1] or not choi.shape[0]:
            raise ValueError("Choi data must be a nonempty square matrix.")
        input_dim = int(np.sqrt(choi.shape[0]))
        output_dim = choi.shape[0] // input_dim
        if input_dim * output_dim != choi.shape[0]:
            raise ValueError("Cannot infer valid channel dimensions.")
        dimensions.append((input_dim, output_dim))

    (input1, output1), (input2, output2) = dimensions
    if output1 != input2:
        raise ValueError("Channel dimensions are incompatible for composition.")

    tensor1 = qml.math.reshape(choi1, (input1, output1, input1, output1))
    tensor2 = qml.math.reshape(choi2, (input2, output2, input2, output2))

    adjoint_choi1 = qml.math.reshape(
        qml.math.transpose(qml.math.conj(tensor1), (1, 0, 3, 2)),
        choi1.shape,
    )
    composed_choi = qml.math.reshape(
        qml.math.einsum("iajb,acbd->icjd", tensor1, tensor2),
        (input1 * output2, input1 * output2),
    )
    return choi1, adjoint_choi1, composed_choi
