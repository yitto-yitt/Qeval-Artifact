# EVAL_META: task_id=125, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()

def circ_to_gate(circ):
    if isinstance(circ, QProg):
        return cast_qprog_to_qcircuit(circ)
    return circ

machine.finalize()
