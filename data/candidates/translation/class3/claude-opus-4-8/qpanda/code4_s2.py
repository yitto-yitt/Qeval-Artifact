# EVAL_META: task_id=4, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QCircuit, matrix_decompose

def create_unitary_from_matrix():
    matrix = np.array([[0, 0, 0, 1], [0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0]], dtype=complex)
    circuit = matrix_decompose([0, 1], matrix)
    return circuit
