# EVAL_META: task_id=60, framework=qpanda, class=3
from pyqpanda3.core import *

def create_cy_gate():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)
    prog = QProg()
    prog << Sdag(q[1]) << CNOT(q[0], q[1]) << S(q[1])
    return prog
