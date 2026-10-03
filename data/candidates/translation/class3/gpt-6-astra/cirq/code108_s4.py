# EVAL_META: task_id=108, framework=cirq, class=3
import cirq
import numpy as np
from math import isqrt


def initialize_adjoint_and_compose(data1, data2):
    def as_choi(data):
        if not isinstance(data, (np.ndarray, list, tuple)):
            operators = cirq.kraus(data, default=None)
            if operators is None:
                unitary = cirq.unitary(data, default=None)
                if unitary is not None:
                    operators = (unitary,)
            if operators is not None:
                operators = tuple(np.asarray(k, dtype=complex) for k in operators)
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
        dimension = isqrt(matrix.shape[0])
        if dimension == 0 or dimension * dimension != matrix.shape[0]:
            raise ValueError("Cannot infer equal input and output dimensions.")
        return matrix, dimension, dimension

    choi1, input1, output1 = as_choi(data1)
    choi2, input2, output2 = as_choi(data2)
    if output1 != input2:
        raise ValueError("Channel dimensions are incompatible for composition.")

    tensor1 = choi1.reshape(input1, output1, input1, output1)
    tensor2 = choi2.reshape(input2, output2, input2, output2)

    adjoint_choi1 = tensor1.conj().transpose(1, 0, 3, 2).reshape(choi1.shape)
    composed_choi = np.einsum(
        "iajb,acbd->icjd", tensor1, tensor2
    ).reshape(input1 * output2, input1 * output2)

    return choi1, adjoint_choi1, composed_choi
