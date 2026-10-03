# EVAL_META: task_id=108, framework=cirq, class=3
import math
import numpy as np
import cirq


def initialize_adjoint_and_compose(data1, data2):
    def as_choi(data):
        kraus_ops = cirq.kraus(data, default=None)
        if kraus_ops is not None:
            kraus_ops = [np.asarray(k, dtype=complex) for k in kraus_ops]
            if not kraus_ops:
                raise ValueError("The channel must have at least one Kraus operator.")
            output_dim, input_dim = kraus_ops[0].shape
            matrix = np.zeros(
                (input_dim * output_dim, input_dim * output_dim), dtype=complex
            )
            for operator in kraus_ops:
                if operator.shape != (output_dim, input_dim):
                    raise ValueError("Kraus operators must have matching dimensions.")
                vector = operator.reshape(-1, order="F")
                matrix += np.outer(vector, vector.conj())
            return matrix, input_dim, output_dim

        matrix = np.array(data, dtype=complex, copy=True)
        if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
            raise ValueError("A Choi matrix must be square.")
        size = matrix.shape[0]
        input_dim = math.isqrt(size)
        if input_dim == 0 or size % input_dim:
            raise ValueError("Invalid Choi matrix dimensions.")
        return matrix, input_dim, size // input_dim

    choi1, input_dim1, output_dim1 = as_choi(data1)
    choi2, input_dim2, output_dim2 = as_choi(data2)

    if output_dim1 != input_dim2:
        raise ValueError("Channel dimensions are incompatible for composition.")

    tensor1 = choi1.reshape(input_dim1, output_dim1, input_dim1, output_dim1)
    tensor2 = choi2.reshape(input_dim2, output_dim2, input_dim2, output_dim2)

    adjoint_choi1 = tensor1.conj().transpose(1, 0, 3, 2).reshape(choi1.shape).copy()
    composed_choi = np.einsum("iajb,acbd->icjd", tensor1, tensor2).reshape(
        input_dim1 * output_dim2, input_dim1 * output_dim2
    )

    return choi1, adjoint_choi1, composed_choi
