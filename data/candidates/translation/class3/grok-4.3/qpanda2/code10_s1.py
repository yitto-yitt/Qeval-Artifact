# EVAL_META: task_id=10, framework=qpanda2, class=3
import numpy as np
from pyqpanda import *
machine = CPUQVM()
machine.initQVM()
qubits = machine.qAlloc_many(2)

def create_operator():
    unitary_matrix = np.array([[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]], dtype=complex)
    return matrix_decompose([qubits[0], qubits[1]], unitary_matrix)

machine.finalize()
