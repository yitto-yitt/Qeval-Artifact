# EVAL_META: task_id=106, framework=qpanda, class=3
from pyqpanda3.core import *

def compose_cnot_dihedral():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)

    circ1 = QCircuit()
    circ1 << CNOT(q[0], q[1]) << T(q[0])

    circ2 = QCircuit()
    circ2 << CNOT(q[0], q[1]) << T(q[0]) << X(q[1])

    composed = QCircuit()
    composed << circ1 << circ2

    machine.finalize()
    return composed
