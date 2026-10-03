# EVAL_META: task_id=118, framework=qpanda, class=3
from math import pi
from pyqpanda3.core import QProg, H, U1

def create_c3sx_circuit():
    prog = QProg()
    prog << H(3)
    prog << U1(3, pi / 2).control([0, 1, 2])
    prog << H(3)
    return prog
