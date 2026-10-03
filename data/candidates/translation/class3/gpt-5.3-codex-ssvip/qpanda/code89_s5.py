# EVAL_META: task_id=89, framework=qpanda, class=3
from pyqpanda3.core import *

def create_controlled_hgate():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(3)

    prog = QProg()
    prog.insert(H(q[2]).control([q[0], q[1]]))

    return prog
