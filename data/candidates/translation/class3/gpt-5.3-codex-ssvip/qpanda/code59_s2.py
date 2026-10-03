# EVAL_META: task_id=59, framework=qpanda, class=3
from pyqpanda3.core import *

def create_cz_gate():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)
    prog = QProg()
    prog << H(q[1]) << CNOT(q[0], q[1]) << H(q[1])
    return prog
