# EVAL_META: task_id=106, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, CNOT, T, X, Qubit

def compose_cnot_dihedral():
    q0 = Qubit(0)
    q1 = Qubit(1)
    circ1 = QCircuit()
    circ1 << CNOT(q0, q1)
    circ1 << T(q0)
    circ2 = QCircuit()
    circ2 << CNOT(q0, q1)
    circ2 << T(q0)
    circ2 << X(q1)
    circ1 << circ2
    return circ1
