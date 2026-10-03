# EVAL_META: task_id=44, framework=qpanda, class=3
from pyqpanda3.core import *

def tensor_circuits():
    machine = CPUQVM()
    machine.init_qvm()

    q_bottom = machine.qAlloc_many(2)
    q_top = machine.qAlloc_many(1)

    prog = QProg()
    prog << CRY(q_bottom[0], q_bottom[1], 0.2)
    prog << X(q_top[0])

    return prog
