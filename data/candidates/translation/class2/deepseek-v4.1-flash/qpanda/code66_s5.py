# EVAL_META: task_id=66, framework=qpanda, class=2
from numpy import arccos, sqrt
from pyqpanda3.core import *


def w_state():
    prog = QProg()
    prog << RY(0, 2 * arccos(1 / sqrt(3)))
    prog << CH(0, 1)
    prog << CNOT(1, 2)
    prog << CNOT(0, 1)
    prog << X(0)
    prog << measure(0, 0)
    prog << measure(1, 1)
    prog << measure(2, 2)
    return prog
