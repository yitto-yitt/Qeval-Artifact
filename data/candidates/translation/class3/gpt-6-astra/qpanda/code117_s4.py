# EVAL_META: task_id=117, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import matrix_decompose


def decompose_unitary(unitary):
    if hasattr(unitary, "to_matrix"):
        unitary = unitary.to_matrix()
    elif hasattr(unitary, "data") and not isinstance(unitary, np.ndarray):
        unitary = unitary.data

    matrix = np.asarray(unitary, dtype=np.complex128)
    if matrix.shape != (4, 4):
        raise ValueError("unitary must be a 4x4 matrix.")

    try:
        return matrix_decompose([0, 1], matrix)
    except TypeError:
        return matrix_decompose(matrix, [0, 1])
