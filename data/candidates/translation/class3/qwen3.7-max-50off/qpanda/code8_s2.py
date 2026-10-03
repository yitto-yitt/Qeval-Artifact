# EVAL_META: task_id=8, framework=qpanda, class=3
from pyqpanda3.core import QProg, qalloc, RX, Parameter

def rx_gate(value=None):
    q = qalloc(1)
    prog = QProg()
    if value is None:
        theta = Parameter("theta")
        prog << RX(q[0], theta)
    else:
        prog << RX(q[0], value)
    return prog
