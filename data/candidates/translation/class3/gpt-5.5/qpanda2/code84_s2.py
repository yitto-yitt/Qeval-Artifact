# EVAL_META: task_id=84, framework=qpanda2, class=3
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)
atexit.register(machine.finalize)

def controlled_custom_unitary_circuit():
    prog = QProg()
    prog << U3(q[1], 0.3, 0.2, 0.1).control([q[0]])
    return prog
