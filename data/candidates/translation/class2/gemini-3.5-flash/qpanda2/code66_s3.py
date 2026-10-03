# EVAL_META: task_id=66, framework=qpanda2, class=2
import pyqpanda as pq
from numpy import arccos, sqrt

_machine = None


def w_state():
    global _machine
    if _machine is None:
        _machine = pq.CPUQVM()
        _machine.init_qvm()

    q = _machine.qAlloc_many(3)
    c = _machine.cAlloc_many(3)

    prog = pq.QProg()
    prog << pq.RY(q[0], 2 * arccos(1 / sqrt(3)))
    prog << pq.CH(q[0], q[1])
    prog << pq.CNOT(q[1], q[2])
    prog << pq.CNOT(q[0], q[1])
    prog << pq.X(q[0])

    prog << pq.Measure(q[0], c[0])
    prog << pq.Measure(q[1], c[1])
    prog << pq.Measure(q[2], c[2])

    return prog
