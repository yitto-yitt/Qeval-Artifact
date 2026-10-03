# EVAL_META: task_id=147, framework=qpanda2, class=3
from pyqpanda import *
import atexit

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(5)
atexit.register(machine.finalize)

def mcy(qc):
    qc.insert(Y(q[4]).control(q[0:4]))
    return qc
