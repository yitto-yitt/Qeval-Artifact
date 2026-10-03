# EVAL_META: task_id=117, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Qubit, matrix_decompose, QMatrix
import numpy as np

def decompose_unitary(unitary):
    q0 = Qubit(0)
    q1 = Qubit(1)
    mat = QMatrix(unitary)
    return matrix_decompose(mat, [q0, q1])

