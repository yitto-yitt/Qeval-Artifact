# EVAL_META: task_id=23, framework=qpanda, class=3
from pyqpanda3.core import *

def dj_constant_oracle():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(3)
    prog = QProg()
    prog << X(q[2])
    qvm.finalize()
    return prog
