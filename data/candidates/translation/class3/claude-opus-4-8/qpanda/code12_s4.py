# EVAL_META: task_id=12, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QCircuit, QProg, H, CNOT, matrix_of_QProg


def get_unitary():
    circ = QCircuit()
    circ << H(0)
    circ << CNOT(0, 1)
    prog = QProg()
    prog << circ
    mat = np.array(matrix_of_QProg(prog)).reshape(4, 4)
    return mat
