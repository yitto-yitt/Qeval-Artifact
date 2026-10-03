# EVAL_META: task_id=125, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(10)


def circ_to_gate(circ):
    return QGate(circ)


machine.finalize()
