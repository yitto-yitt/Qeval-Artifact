# EVAL_META: task_id=106, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit


def compose_cnot_dihedral():
    circ1 = QuantumCircuit(2)
    circ1.cx(0, 1)
    circ1.t(0)
    elem1 = circ1
    circ2 = circ1.copy()
    circ2.x(1)
    elem2 = circ2
    composed_elem = elem1.compose(elem2)
    return composed_elem
