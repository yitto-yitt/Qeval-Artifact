# EVAL_META: task_id=147, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(5)

def mcy(qc):
    gate = Y(q[4])
    for ctrl in (q[0], q[1], q[2], q[3]):
        gate = gate.control(ctrl)
    qc << gate
    return qc

machine.finalize()
