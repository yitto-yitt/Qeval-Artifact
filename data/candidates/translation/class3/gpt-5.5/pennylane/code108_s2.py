# EVAL_META: task_id=108, framework=pennylane, class=3
import pennylane as qml
import numpy as np


def initialize_adjoint_and_compose(data1, data2):
    def _as_choi_array(data):
        return np.array(data, dtype=complex, copy=True)

    def _infer_equal_dims(choi):
        if choi.ndim != 2 or choi.shape[0] != choi.shape[1]:
            raise ValueError("Choi data must be a square matrix.")
        dim = int(round(np.sqrt(choi.shape[0])))
        if dim * dim != choi.shape[0]:
            raise ValueError("Cannot infer equal input and output dimensions.")
        return dim, dim

    def _choi_to_superop(choi, input_dim, output_dim):
        return np.reshape(choi, (input_dim, output_dim, input_dim, output_dim)).transpose(1, 3, 0, 2).reshape(
            output_dim * output_dim, input_dim * input_dim
        )

    def _superop_to_choi(superop, input_dim, output_dim):
        return np.reshape(superop, (output_dim, output_dim, input_dim, input_dim)).transpose(2, 0, 3, 1).reshape(
            input_dim * output_dim, input_dim * output_dim
        )

    choi1 = _as_choi_array(data1)
    choi2 = _as_choi_array(data2)

    input_dim1, output_dim1 = _infer_equal_dims(choi1)
    input_dim2, output_dim2 = _infer_equal_dims(choi2)

    superop1 = _choi_to_superop(choi1, input_dim1, output_dim1)
    superop2 = _choi_to_superop(choi2, input_dim2, output_dim2)

    adjoint_choi1 = _superop_to_choi(superop1.conj().T, output_dim1, input_dim1)
    composed_choi = _superop_to_choi(superop1 @ superop2, input_dim2, output_dim1)

    return choi1, adjoint_choi1, composed_choi
