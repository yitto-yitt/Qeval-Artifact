# EVAL_META: task_id=41, framework=qpanda2, class=3
import numpy as np
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def compose_op():
    I = np.eye(2)
    X = np.array([[0, 1], [1, 0]])
    Y = np.array([[0, -1j], [1j, 0]])
    matrix = np.kron(X, np.kron(I, Y))
    op = QOperator(matrix)
    return op

machine.finalize()
