# EVAL_META: task_id=8, framework=qpanda, class=3
from pyqpanda3.core import *

def rx_gate(value=None):
    theta = var(0.0, "theta")
    q = qAlloc_many(1)
    prog = QProg()
    if value is not None:
        prog << RX(q[0], float(value))
    else:
        prog << RX(q[0], theta)
    return prog
