# EVAL_META: task_id=106, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit

def compose_cnot_dihedral():
    circ = QuantumCircuit(2)
    circ.cx(0, 1)
    circ.t(0)
    circ.cx(0, 1)
    circ.t(0)
    circ.x(1)
    return circ
