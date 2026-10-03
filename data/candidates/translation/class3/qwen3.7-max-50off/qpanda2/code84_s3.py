# EVAL_META: task_id=84, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init()
q = machine.qAlloc_many(2)

def controlled_custom_unitary_circuit():
    prog = QProg()
    prog << CU(q[0], q[1], 0.3, 0.2, 0.1, 0.0)
    return prog

machine.finalize()
