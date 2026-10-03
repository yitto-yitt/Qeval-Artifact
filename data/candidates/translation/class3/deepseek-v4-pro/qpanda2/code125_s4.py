# EVAL_META: task_id=125, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
_q = machine.qAlloc_many(1)


def circ_to_gate(circ):
    return QGate(circ)


machine.finalize()
