# EVAL_META: task_id=106, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit


def compose_cnot_dihedral():
    circ1 = QuantumCircuit(2)
    circ1.cx(0, 1)
    circ1.t(0)

    circ2 = QuantumCircuit(2)
    circ2.cx(0, 1)
    circ2.t(0)
    circ2.x(1)

    composed = QuantumCircuit(2)
    composed.cx(0, 1)
    composed.t(0)
    composed.cx(0, 1)
    composed.t(0)
    composed.x(1)
    return composed
