# EVAL_META: task_id=145, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(20)
def qft_inverse(n):
    return QFT(q[:n], inverse=True)
machine.finalize()
