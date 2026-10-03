# EVAL_META: task_id=118, framework=qpanda, class=3
from pyqpanda3 import *

def create_c3sx_circuit():
    init(QMachineType.CPU)
    q = qAlloc_many(4)
    prog = QProg()
    prog << C3SXGate(q[0], q[1], q[2], q[3])
    return prog
