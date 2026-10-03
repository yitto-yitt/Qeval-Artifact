# EVAL_META: task_id=108, framework=cirq, class=3
import math
import numpy as np
import cirq


def initialize_adjoint_and_compose(data1, data2):
    def to_choi(data):
        if not isinstance(data, (np.ndarray, list, tuple)):
            kraus = cirq.kraus(data, default=None)
            if kraus is not None:
                operators = [np.asarray(k, dtype=complex) for k in kraus]
                if not operators:
                    raise ValueError("A channel must have at least one Kraus operator.")
                output_dim, input_dim = operators[0].shape
                vectors = np.stack(
                    [k.reshape(-1, order="F") for k in operators]
                )
                matrix = vectors.T @ vectors.conj()
                return matrix, input_dim, output_dim

        matrix = np.array(data, dtype=complex, copy=True)
        if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
            raise ValueError("A Choi matrix must be square.")
        dim = math.isqrt(matrix.shape[0])
        if dim == 0 or dim * dim != matrix.shape[0]:
            raise ValueError("Cannot infer equal input and output dimensions.")
        return matrix, dim, dim

    choi1, input1, output1 = to_choi(data1)
    choi2, input2, output2 = to_choi(data2)

    if output1 != input2:
        raise ValueError("Channel dimensions are incompatible for composition.")

    tensor1 = choi1.reshape(input1, output1, input1, output1)
    tensor2 = choi2.reshape(input2, output2, input2, output2)

    adjoint_choi1 = tensor1.conj().transpose(1, 0, 3, 2).reshape(
        output1 * input1, output1 * input1
    )
    composed_choi = np.einsum(
        "iajb,acbd->icjd", tensor1, tensor2, optimize=True
    ).reshape(input1 * output2, input1 * output2)

    return choi1, adjoint_choi1, composed_choi
