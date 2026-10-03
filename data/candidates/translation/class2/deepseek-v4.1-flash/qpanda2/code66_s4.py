# EVAL_META: task_id=66, framework=qpanda2, class=2
from numpy import arccos, sqrt
from pyqpanda import *


def w_state():
    q = initQubits(3)
    c = initClassicalBits(3)
    prog = QProg()
    prog << RY(2 * arccos(1 / sqrt(3)), q[0])
    prog << CH(q[0], q[1])
    prog << CNOT(q[1], q[2])
    prog << CNOT(q[0], q[1])
    prog << X(q[0])
    prog << Measure(q[0], c[0]) << Measure(q[1], c[1]) << Measure(q[2], c[2])
    return prog
