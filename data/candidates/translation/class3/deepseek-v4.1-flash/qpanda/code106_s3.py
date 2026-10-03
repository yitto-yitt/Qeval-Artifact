# EVAL_META: task_id=106, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, CNOT, T, X, CNOTDihedral

def compose_cnot_dihedral():
    circ1 = QCircuit()
    circ1 << CNOT(0, 1)
    circ1 << T(0)
    elem1 = CNOTDihedral(circ1)

    circ2 = QCircuit()
    circ2 << CNOT(0, 1)
    circ2 << T(0)
    circ2 << X(1)
    elem2 = CNOTDihedral(circ2)

    composed_elem = elem1.compose(elem2)
    return composed_elem
