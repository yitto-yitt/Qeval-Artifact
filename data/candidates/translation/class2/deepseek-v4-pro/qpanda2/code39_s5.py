# EVAL_META: task_id=39, framework=qpanda2, class=2
from pyqpanda import *

def create_uniform_superposition(n):
    init(QMachineType.CPU)
    q = qAlloc_many(n)
    prog = QProg()
    for i in range(n):
        prog << H(q[i])
    return get_qstate(prog, q, -1)
