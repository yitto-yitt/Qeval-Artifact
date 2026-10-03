# EVAL_META: task_id=106, framework=qpanda, class=3
from pyqpanda3.core import *

def compose_cnot_dihedral():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)

    prog1 = QProg()
    prog1 << CNOT(q[0], q[1]) << T(q[0])

    prog2 = QProg()
    prog2 << CNOT(q[0], q[1]) << T(q[0]) << X(q[1])

    composed_prog = QProg()
    composed_prog << prog1 << prog2

    return composed_prog
