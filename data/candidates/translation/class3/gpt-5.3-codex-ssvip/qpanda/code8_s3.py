# EVAL_META: task_id=8, framework=qpanda, class=3
from pyqpanda3.core import *

def rx_gate(value=None):
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(1)
    prog = QProg()
    theta = var(0.0)
    prog << RX(q[0], theta)
    if value is not None:
        theta.set_value(float(value))
    return prog
