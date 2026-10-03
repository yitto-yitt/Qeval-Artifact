# EVAL_META: task_id=106, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QGate

def compose_cnot_dihedral():
    circ = QCircuit()
    circ << QGate("CNOT", [0, 1])
    circ << QGate("T", 0)
    circ << QGate("CNOT", [0, 1])
    circ << QGate("T", 0)
    circ << QGate("X", 1)
    return circ
