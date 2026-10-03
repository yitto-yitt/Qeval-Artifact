# EVAL_META: task_id=5, framework=qpanda, class=2
from pyqpanda3.core import CPUQVM, QProg, X

def create_state_prep():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)
    prog = QProg()
    prog << X(q[0])
    return prog
