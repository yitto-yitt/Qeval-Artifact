# EVAL_META: task_id=108, framework=pennylane, class=3
import math
import pennylane as qml


def initialize_adjoint_and_compose(data1, data2):
    choi1 = qml.math.array(data1, dtype=complex, like="numpy")
    choi2 = qml.math.array(data2, dtype=complex, like="numpy")

    dimensions = []
    for choi in (choi1, choi2):
        if choi.ndim != 2 or choi.shape[0] != choi.shape[1]:
            raise ValueError("Choi matrices must be square.")
        size = choi.shape[0]
        input_dim = math.isqrt(size)
        if input_dim == 0 or size % input_dim:
            raise ValueError("Cannot infer compatible channel dimensions.")
        dimensions.append((input_dim, size // input_dim))

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
