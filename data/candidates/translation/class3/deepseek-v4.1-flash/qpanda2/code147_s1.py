# EVAL_META: task_id=147, framework=qpanda2, class=3
from pyqpanda import *

qvm = CPUQVM()
qvm.init_qvm()
q = qvm.qAlloc_many(5)

def mcy(qc):
    qc << Y(q[4]).control([q[0], q[1], q[2], q[3]])
    return qc

qvm.finalize()
