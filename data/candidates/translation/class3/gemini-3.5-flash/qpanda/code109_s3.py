# EVAL_META: task_id=109, framework=qpanda, class=3
from pyqpanda3.core import *

def circuit():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(1)
    theta = var(0.0, True)
    
    prog = QProg()
    prog << H(q[0]) << RZ(q[0], theta)
    return prog
