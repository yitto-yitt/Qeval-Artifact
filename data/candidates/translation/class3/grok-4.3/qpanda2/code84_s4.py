# EVAL_META: task_id=84, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.initQVM()
qlist = machine.qAlloc_many(2)

def controlled_custom_unitary_circuit():
    prog = QProg()
    prog << CU(0.3, 0.2, 0.1, qlist[0], qlist[1])
    return prog

machine.finalize()
