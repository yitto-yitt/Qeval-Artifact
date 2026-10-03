# EVAL_META: task_id=5, framework=qpanda2, class=2
from pyqpanda import QCircuit, X, I, Qubit

def create_state_prep():
    circ = QCircuit()
    circ << X(Qubit(0))
    circ << I(Qubit(1))
    return circ
