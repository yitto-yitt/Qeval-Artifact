# EVAL_META: task_id=66, framework=qpanda2, class=2
import pyqpanda as pq
from numpy import arccos, sqrt


def w_state():
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(3)
    c = machine.cAlloc_many(3)

    prog = pq.QProg()
    prog << pq.RY(q[0], 2 * arccos(1 / sqrt(3)))
    prog << pq.H(q[1]).control([q[0]])
    prog << pq.CNOT(q[1], q[2])
    prog << pq.CNOT(q[0], q[1])
    prog << pq.X(q[0])

    for i in range(3):
        prog << pq.Measure(q[i], c[i])

    return prog
