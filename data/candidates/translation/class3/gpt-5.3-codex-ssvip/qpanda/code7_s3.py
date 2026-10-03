# EVAL_META: task_id=7, framework=qpanda, class=3
from pyqpanda3.core import *

def create_parametrized_gate():
    theta = var(0.0, "theta")
    q = qalloc(1)
    prog = QProg()
    prog << RX(q[0], theta)
    return prog
