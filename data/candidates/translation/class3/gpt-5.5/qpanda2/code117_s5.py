# EVAL_META: task_id=117, framework=qpanda2, class=3
import atexit
import numpy as np
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)
atexit.register(machine.finalize)

def decompose_unitary(unitary):
    if hasattr(unitary, "data"):
        matrix = unitary.data
    elif hasattr(unitary, "to_matrix"):
        matrix = unitary.to_matrix()
    else:
        matrix = unitary
    matrix = np.asarray(matrix, dtype=np.complex128)
    return matrix_decompose(q, matrix.tolist())
