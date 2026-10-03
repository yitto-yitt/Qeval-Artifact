# EVAL_META: task_id=117, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import matrix_decompose


def decompose_unitary(unitary):
    matrix = np.asarray(unitary, dtype=np.complex128)
    return matrix_decompose([0, 1], matrix)
