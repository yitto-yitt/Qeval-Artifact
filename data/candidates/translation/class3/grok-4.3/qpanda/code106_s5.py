# EVAL_META: task_id=106, framework=qpanda, class=3
from pyqpanda3.core import *

def compose_cnot_dihedral():
    circ1 = QCircuit()
    circ1 << CNOT(0, 1) << T(0)
    circ2 = QCircuit(circ1)
    circ2 << X(1)
    composed = circ1.compose(circ2)
    return composed
