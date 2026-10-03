# EVAL_META: task_id=12, framework=qpanda, class=3
import pyqpanda3.core as pq
import numpy as np


def get_unitary():
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1])
    mat = pq.get_circuit_matrix(prog)
    return np.array(mat).reshape(4, 4)
