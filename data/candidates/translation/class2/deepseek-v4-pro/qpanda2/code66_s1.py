# EVAL_META: task_id=66, framework=qpanda2, class=2
from math import acos, sqrt
from pyqpanda import *


def w_state():
    init(QMachineType.CPU)
    q = qAlloc_many(3)
    c = cAlloc_many(3)

    prog = QProg()
    prog << RY(q[0], 2 * acos(1 / sqrt(3)))
    prog << CH(q[0], q[1])
    prog << CNOT(q[1], q[2])
    prog << CNOT(q[0], q[1])
    prog << X(q[0])
    prog << MeasureAll(q, c)

    return prog
