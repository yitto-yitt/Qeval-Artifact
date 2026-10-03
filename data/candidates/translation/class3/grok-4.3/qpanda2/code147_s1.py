# EVAL_META: task_id=147, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(5)
def mcy(qc):
    mcy_gate = Y(q[4]).control(q[0:4])
    qc << mcy_gate
    return qc
machine.finalize()
