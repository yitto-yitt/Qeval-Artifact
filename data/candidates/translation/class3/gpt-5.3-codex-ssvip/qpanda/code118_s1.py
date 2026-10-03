# EVAL_META: task_id=118, framework=qpanda, class=3
from pyqpanda3.core import *

def create_c3sx_circuit():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(4)
    prog = QProg()
    prog << C3X(q[0], q[1], q[2], q[3]) << SX(q[3])
    return prog
