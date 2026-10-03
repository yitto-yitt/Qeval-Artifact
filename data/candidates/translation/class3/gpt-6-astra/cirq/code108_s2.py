# EVAL_META: task_id=108, framework=cirq, class=3
import math
import numpy as np
import cirq


def initialize_adjoint_and_compose(data1, data2):
    def as_choi(data):
        if not isinstance(data, (list, tuple, np.ndarray)):
            kraus = cirq.kraus(data, default=None)
            if kraus is not None:
                operators = [np.asarray(k, dtype=complex) for k in kraus]
                output_dim, input_dim = operators[0].shape
                matrix = np.zeros(
                    (input_dim * output_dim, input_dim * output_dim),
                    dtype=complex,
                )
                for operator in operators:
                    vector = operator.reshape(-1, order="F")
                    matrix += np.outer(vector, vector.conj())
                return matrix, input_dim, output_dim

        matrix = np.array(data, dtype=complex, copy=True)
        if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
            raise ValueError("A Choi matrix must be square.")
        size = matrix.shape[0]
        input_dim = math.isqrt(size)
        if input_dim == 0 or size % input_dim:
            raise ValueError("Cannot infer valid channel dimensions.")
        return matrix, input_dim, size // input_dim

    choi1, input1, output1 = as_choi(data1)
    choi2, input2, output2 = as_choi(data2)

    if output1 != input2:
        raise ValueError("Channel dimensions are incompatible for composition.")

    tensor1 = choi1.reshape(input1, output1, input1, output1)
    tensor2 = choi2.reshape(input2, output2, input2, output2)

    adjoint_choi1 = tensor1.conj().transpose(1, 0, 3, 2).reshape(choi1.shape)
    composed_choi = np.einsum(
        "ikjl,kalb->iajb", tensor1, tensor2
    ).reshape(input1 * output2, input1 * output2)

    return choi1, adjoint_choi1, composed_choi
