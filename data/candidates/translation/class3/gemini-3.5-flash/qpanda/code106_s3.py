# EVAL_META: task_id=106, framework=qpanda, class=3
from pyqpanda3.core import *


def compose_cnot_dihedral():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)

    prog = QProg()
    prog << CNOT(q[0], q[1])
    prog << T(q[0])
    prog << CNOT(q[0], q[1])
    prog << T(q[0])
    prog << X(q[1])

    return prog
