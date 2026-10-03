# EVAL_META: task_id=5, framework=qpanda, class=2
from pyqpanda3.core import QCircuit, X

def create_state_prep():
    circ = QCircuit(2)
    circ << X(0)
    return circ
