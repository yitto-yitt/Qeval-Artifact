# EVAL_META: task_id=117, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import unitary_decomposer

def decompose_unitary(unitary):
    matrix = np.asarray(unitary, dtype=complex).tolist()
    return unitary_decomposer(matrix, 2)

