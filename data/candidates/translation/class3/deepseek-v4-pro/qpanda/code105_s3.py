# EVAL_META: task_id=105, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit


def initialize_cnot_dihedral():
    circ = QuantumCircuit(2)
    circ.cx(0, 1)
    circ.t(0)
    return circ
