# EVAL_META: task_id=106, framework=qpanda, class=3
from pyqpanda3.core import CNOT, CPUQVM, QCircuit, T, X


def compose_cnot_dihedral():
    qvm = CPUQVM()
    qvm.init()
    q = qvm.qAlloc_many(2)

    circ1 = QCircuit()
    circ1 << CNOT(q[0], q[1]) << T(q[0])

    circ2 = QCircuit()
    circ2 << CNOT(q[0], q[1]) << T(q[0]) << X(q[1])

    composed = QCircuit()
    composed << CNOT(q[0], q[1]) << T(q[0])
    composed << CNOT(q[0], q[1]) << T(q[0]) << X(q[1])

    return composed
