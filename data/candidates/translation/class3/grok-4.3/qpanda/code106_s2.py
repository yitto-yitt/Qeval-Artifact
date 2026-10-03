# EVAL_META: task_id=106, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, CNOT, T, X


def compose_cnot_dihedral():
    circ1 = QCircuit(2)
    circ1.insert(CNOT(0, 1))
    circ1.insert(T(0))
    circ2 = circ1.copy()
    circ2.insert(X(1))
    composed = circ1.compose(circ2)
    return composed
