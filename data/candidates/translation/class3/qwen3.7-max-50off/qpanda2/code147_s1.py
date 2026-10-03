# EVAL_META: task_id=147, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(5)

def mcy(qc):
    qc << Y(q[4])
    return qc

machine.finalize()
