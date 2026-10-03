# EVAL_META: task_id=4, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QCircuit, QGate, matrix_decompose, QMatrix

def create_unitary_from_matrix():
    matrix = [[0, 0, 0, 1], [0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0]]
    qmat = QMatrix(np.array(matrix, dtype=complex))
    circuit = matrix_decompose([0, 1], qmat)
    return circuit
