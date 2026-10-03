# EVAL_META: task_id=12, framework=qpanda, class=3
import pyqpanda3.core as pq
import numpy as np


def get_unitary():
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    prog = pq.QProg()
    prog << pq.H(q[1]) << pq.CNOT(q[1], q[0])
    u = pq.get_unitary(prog)
    return np.array(u).reshape(4, 4)
