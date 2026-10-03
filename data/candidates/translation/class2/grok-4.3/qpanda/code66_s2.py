# EVAL_META: task_id=66, framework=qpanda, class=2
from numpy import arccos, sqrt
from pyqpanda3.core import CPUQVM, create_empty_qprog, RY, H, CNOT, X, Measure


def w_state():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(3)
    c = qvm.cAlloc_many(3)
    prog = create_empty_qprog()
    prog << RY(q[0], 2 * arccos(1 / sqrt(3)))
    prog << H(q[1]).control(q[0])
    prog << CNOT(q[1], q[2])
    prog << CNOT(q[0], q[1])
    prog << X(q[0])
    for i in range(3):
        prog << Measure(q[i], c[i])
    return prog
