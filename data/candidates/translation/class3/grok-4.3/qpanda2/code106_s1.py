# EVAL_META: task_id=106, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)
def compose_cnot_dihedral():
    circ1 = QCircuit()
    circ1 << CNOT(q[0], q[1])
    circ1 << T(q[0])
    circ2 = QCircuit()
    circ2 << CNOT(q[0], q[1])
    circ2 << T(q[0])
    circ2 << X(q[1])
    composed = circ1 + circ2
    return composed
machine.finalize()
