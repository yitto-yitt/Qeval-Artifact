# EVAL_META: task_id=5, framework=qpanda, class=2
from pyqpanda3.core import QCircuit, qAlloc, X

def create_state_prep():
    q = qAlloc(2)
    circ = QCircuit()
    circ << X(q[0])
    return circ
