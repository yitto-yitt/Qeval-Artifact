# EVAL_META: task_id=109, framework=qpanda, class=3
from pyqpanda3.core import *

def circuit():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(1)
    prog = QProg()
    prog.insert(H(q[0]))
    theta = var(0.0)
    prog.insert(RZ(q[0], theta))
    return prog
