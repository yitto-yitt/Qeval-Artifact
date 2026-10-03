# EVAL_META: task_id=4, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def create_unitary_from_matrix():
    matrix = np.array([[0, 0, 0, 1],
                       [0, 0, 1, 0],
                       [1, 0, 0, 0],
                       [0, 1, 0, 0]], dtype=complex)
    prog = pq.QProg()
    prog << pq.QOracle(q, matrix)
    return prog

machine.finalize()
