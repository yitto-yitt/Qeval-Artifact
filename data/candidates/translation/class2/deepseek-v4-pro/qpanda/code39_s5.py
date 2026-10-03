# EVAL_META: task_id=39, framework=qpanda, class=2
from pyqpanda3.core import *

def create_uniform_superposition(n):
    init(QMachineType.CPU)
    q = qAlloc_many(n)
    prog = QProg()
    for i in range(n):
        prog << H(q[i])
    return getStatevector(prog)
