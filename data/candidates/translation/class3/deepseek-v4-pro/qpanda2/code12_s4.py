# EVAL_META: task_id=12, framework=qpanda2, class=3
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def get_unitary():
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])
    return machine.get_matrix(prog, q)

atexit.register(machine.finalize)
