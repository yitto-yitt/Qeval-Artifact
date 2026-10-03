# EVAL_META: task_id=147, framework=qpanda2, class=3
from pyqpanda import *
import atexit

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(5)

def mcy(qc):
    ctrl_y = Y(q[4]).control([q[0], q[1], q[2], q[3]])
    qc << ctrl_y
    return qc

atexit.register(machine.finalize)
