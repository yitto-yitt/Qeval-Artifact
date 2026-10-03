# EVAL_META: task_id=66, framework=qpanda, class=2
from pyqpanda3.core import QProg, QVec, CVec, RY, H, X, CNOT, Measure
from numpy import arccos, sqrt

def w_state():
    q = QVec(3)
    c = CVec(3)
    prog = QProg()
    prog << RY(q[0], 2 * arccos(1 / sqrt(3)))
    prog << H(q[1]).control(q[0])
    prog << CNOT(q[1], q[2])
    prog << CNOT(q[0], q[1])
    prog << X(q[0])
    for i in range(3):
        prog << Measure(q[i], c[i])
    return prog
