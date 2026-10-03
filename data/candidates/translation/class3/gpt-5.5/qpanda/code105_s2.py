# EVAL_META: task_id=105, framework=qpanda, class=3
from pyqpanda3.core import *


def initialize_cnot_dihedral():
    circ = QCircuit()
    circ << CNOT(0, 1)
    circ << T(0)
    return circ
