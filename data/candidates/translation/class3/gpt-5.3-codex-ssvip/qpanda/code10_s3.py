# EVAL_META: task_id=10, framework=qpanda, class=3
from pyqpanda3.core import *

def create_operator():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)

    prog = QProg()
    prog << X(q[0]) << X(q[1])

    machine.finalize()
    return prog
