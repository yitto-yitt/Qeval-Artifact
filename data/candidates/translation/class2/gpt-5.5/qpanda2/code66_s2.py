# EVAL_META: task_id=66, framework=qpanda2, class=2
from numpy import arccos, sqrt
import pyqpanda as pq


def w_state():
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(3)
    c = qvm.cAlloc_many(3)

    prog = pq.QProg()
    prog << pq.RY(q[0], 2 * arccos(1 / sqrt(3)))
    prog << pq.H(q[1]).control([q[0]])
    prog << pq.CNOT(q[1], q[2])
    prog << pq.CNOT(q[0], q[1])
    prog << pq.X(q[0])
    prog << pq.measure_all(q, c)

    w_state._qvm = qvm
    return prog
