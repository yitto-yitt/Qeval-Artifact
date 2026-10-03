# EVAL_META: task_id=10, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit

def create_operator():
    circ = QuantumCircuit(2)
    circ.x(0)
    circ.x(1)
    return circ
