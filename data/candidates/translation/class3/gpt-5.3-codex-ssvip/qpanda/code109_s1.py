# EVAL_META: task_id=109, framework=qpanda, class=3
from pyqpanda3.core import *

def circuit():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(1)
    prog = QProg()
    prog << H(q[0])
    theta = Var("th")
    prog << RZ(q[0], theta)
    return prog
