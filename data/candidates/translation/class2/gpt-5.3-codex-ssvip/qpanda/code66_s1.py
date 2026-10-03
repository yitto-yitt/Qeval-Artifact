# EVAL_META: task_id=66, framework=qpanda, class=2
from numpy import arccos, sqrt
from pyqpanda3.core import *

def w_state():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(3)
    c = machine.cAlloc_many(3)

    prog = QProg()
    prog << RY(q[0], 2 * arccos(1 / sqrt(3)))
    prog << CH(q[0], q[1])
    prog << CNOT(q[1], q[2])
    prog << CNOT(q[0], q[1])
    prog << X(q[0])
    prog << MeasureAll(q, c)

    machine.finalize()
    return prog
