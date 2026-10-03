# EVAL_META: task_id=105, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, CNOT, T


def initialize_cnot_dihedral():
    circ = QCircuit(2)
    circ << CNOT(0, 1)
    circ << T(0)
    return circ
