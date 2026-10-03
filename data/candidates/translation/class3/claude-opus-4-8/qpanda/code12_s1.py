# EVAL_META: task_id=12, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QCircuit, QProg, H, CNOT, matrix_to_array


def get_unitary():
    qc = QCircuit(2)
    qc << H(0)
    qc << CNOT(0, 1)
    prog = QProg()
    prog << qc
    mat = matrix_to_array(prog.matrix())
    return np.array(mat).reshape(4, 4)
