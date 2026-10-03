# EVAL_META: task_id=44, framework=qpanda, class=3
from pyqpanda3.core import *

def tensor_circuits():
    machine = CPUQVM()
    machine.init_qvm()

    top_q = machine.qAlloc_many(1)
    bottom_q = machine.qAlloc_many(2)

    top_prog = QProg()
    top_prog << X(top_q[0])

    bottom_prog = QProg()
    bottom_prog << CRY(bottom_q[0], bottom_q[1], 0.2)

    tensored = QProg()
    tensored << bottom_prog << top_prog

    return tensored
