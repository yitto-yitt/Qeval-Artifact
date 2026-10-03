# EVAL_META: task_id=10, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit

def create_operator():
    circ = QuantumCircuit(2, 2)
    circ.cx(0, 1)
    circ.cx(1, 0)
    circ.cx(0, 1)
    return circ
