# EVAL_META: task_id=4, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import CPUQVM, QProg, matrix_decompose

def create_unitary_from_matrix():
    matrix = np.array(
        [[0, 0, 0, 1],
         [0, 0, 1, 0],
         [1, 0, 0, 0],
         [0, 1, 0, 0]],
        dtype=complex
    )
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)
    prog = QProg()
    prog.insert(matrix_decompose(q, matrix.tolist()))
    return prog
