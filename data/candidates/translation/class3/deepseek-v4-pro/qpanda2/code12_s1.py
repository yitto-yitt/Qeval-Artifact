# EVAL_META: task_id=12, framework=qpanda2, class=3
import atexit
import numpy as np
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def get_unitary():
    unitary = np.zeros((4, 4), dtype=complex)
    for i in range(4):
        prog = QProg()
        if i & 1:
            prog << X(q[0])
        if i & 2:
            prog << X(q[1])
        prog << H(q[0])
        prog << CNOT(q[0], q[1])
        machine.directly_run(prog)
        state = np.asarray(machine.get_qstate(), dtype=complex).reshape(4)
        unitary[:, i] = state
    return unitary

atexit.register(machine.finalize)
