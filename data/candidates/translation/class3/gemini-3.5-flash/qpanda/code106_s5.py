# EVAL_META: task_id=106, framework=qpanda, class=3
from pyqpanda3.core import *


def compose_cnot_dihedral():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)

    prog1 = QProg()
    prog1 << CNOT(q[0], q[1]) << T(q[0])
    elem1 = CNOTDihedral(prog1)

    prog2 = QProg()
    prog2 << CNOT(q[0], q[1]) << T(q[0]) << X(q[1])
    elem2 = CNOTDihedral(prog2)

    composed_elem = elem1.compose(elem2)
    return composed_elem
