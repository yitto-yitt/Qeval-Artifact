# EVAL_META: task_id=105, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, CNOT, T, Qubit, CNOTDihedral


def initialize_cnot_dihedral():
    q0 = Qubit(0)
    q1 = Qubit(1)
    circ = QCircuit()
    circ << CNOT(q0, q1)
    circ << T(q0)
    elem = CNOTDihedral(circ)
    return elem
