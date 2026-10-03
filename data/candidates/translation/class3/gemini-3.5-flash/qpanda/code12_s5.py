# EVAL_META: task_id=12, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq


def get_unitary():
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1])

    matrix = pq.get_circuit_matrix(prog, True)
    matrix = np.array(matrix)
    if len(matrix.shape) == 1:
        n = int(np.sqrt(len(matrix)))
        matrix = matrix.reshape((n, n))
    return matrix
