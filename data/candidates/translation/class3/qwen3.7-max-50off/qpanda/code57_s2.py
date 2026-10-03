# EVAL_META: task_id=57, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Qubit, CNOT

def create_swap_gate():
    q0 = Qubit()
    q1 = Qubit()
    circ = QCircuit()
    circ << CNOT(q0, q1)
    circ << CNOT(q1, q0)
    circ << CNOT(q0, q1)
    return circ
