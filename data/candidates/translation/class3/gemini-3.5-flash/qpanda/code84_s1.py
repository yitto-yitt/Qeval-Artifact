# EVAL_META: task_id=84, framework=qpanda, class=3
from pyqpanda3.core import *

def controlled_custom_unitary_circuit():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qalloc_many(2)
    prog = QProg()
    gate = U3(q[1], 0.3, 0.2, 0.1)
    controlled_gate = gate.control(q[0:1])
    prog.insert(controlled_gate)
    return prog
