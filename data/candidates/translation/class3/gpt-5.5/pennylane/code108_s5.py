# EVAL_META: task_id=108, framework=pennylane, class=3
import math
from pennylane import numpy as np


def initialize_adjoint_and_compose(data1, data2):
    choi1 = np.array(data1, dtype=complex)
    choi2 = np.array(data2, dtype=complex)

    def _infer_dim(choi):
        if len(choi.shape) != 2 or choi.shape[0] != choi.shape[1]:
            raise ValueError("Choi data must be a square matrix.")
        dim = int(round(math.sqrt(int(choi.shape[0]))))
        if dim * dim != int(choi.shape[0]):
            raise ValueError("Cannot infer equal input and output dimensions.")
        return dim, dim

    def _choi_to_superop(choi, input_dim, output_dim):
        return np.transpose(
            np.reshape(choi, (output_dim, input_dim, output_dim, input_dim)),
            (0, 2, 1, 3),
        ).reshape((output_dim * output_dim, input_dim * input_dim))

    def _superop_to_choi(superop, input_dim, output_dim):
        return np.transpose(
            np.reshape(superop, (output_dim, output_dim, input_dim, input_dim)),
            (0, 2, 1, 3),
        ).reshape((output_dim * input_dim, output_dim * input_dim))

    in1, out1 = _infer_dim(choi1)
    in2, out2 = _infer_dim(choi2)

    superop1 = _choi_to_superop(choi1, in1, out1)
    superop2 = _choi_to_superop(choi2, in2, out2)

    adjoint_choi1 = _superop_to_choi(np.conjugate(np.transpose(superop1)), out1, in1)
    composed_choi = _superop_to_choi(superop2 @ superop1, in1, out2)

    return choi1, adjoint_choi1, composed_choi
