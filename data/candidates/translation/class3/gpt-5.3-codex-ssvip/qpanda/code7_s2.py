# EVAL_META: task_id=7, framework=qpanda, class=3
from pyqpanda3.core import *


def create_parametrized_gate():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(1)

    theta = var(0.0)
    prog = QProg()
    prog << RX(q[0], theta)

    return prog
