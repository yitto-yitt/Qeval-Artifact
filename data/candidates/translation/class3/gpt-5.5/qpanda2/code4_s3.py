# EVAL_META: task_id=4, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np
import atexit

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def create_unitary_from_matrix():
    matrix = np.array(
        [[0, 0, 0, 1],
         [0, 0, 1, 0],
         [1, 0, 0, 0],
         [0, 1, 0, 0]],
        dtype=complex
    )
    return matrix_decompose(qubits, matrix)

atexit.register(machine.finalize)
