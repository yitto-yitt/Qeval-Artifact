# EVAL_META: task_id=105, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Qubit, CNOT, T

def initialize_cnot_dihedral():
    q0 = Qubit()
    q1 = Qubit()
    circ = QCircuit()
    circ.insert(CNOT(q0, q1))
    circ.insert(T(q0))
    return circ
