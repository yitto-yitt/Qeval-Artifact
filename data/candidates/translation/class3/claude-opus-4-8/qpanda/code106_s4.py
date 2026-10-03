# EVAL_META: task_id=106, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, CNOT, T, X


def compose_cnot_dihedral():
    circ1 = QCircuit(2)
    circ1 << CNOT(0, 1)
    circ1 << T(0)

    circ2 = QCircuit(2)
    circ2 << CNOT(0, 1)
    circ2 << T(0)
    circ2 << X(1)

    composed = QCircuit(2)
    composed << circ1
    composed << circ2

    prog = QProg()
    prog << composed
    return prog
