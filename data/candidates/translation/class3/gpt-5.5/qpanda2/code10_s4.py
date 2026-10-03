# EVAL_META: task_id=10, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)
c = machine.cAlloc_many(2)

def create_operator():
    prog = QProg()
    prog << X(q[0]) << X(q[1])
    return prog

machine.finalize()
