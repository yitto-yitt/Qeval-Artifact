# EVAL_META: task_id=10, framework=qpanda, class=3
from pyqpanda3.core import *
import numpy as np

def create_operator():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)
    unitary = np.array([[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]])
    circ = matrix_decompose(q, unitary)
    return circ
