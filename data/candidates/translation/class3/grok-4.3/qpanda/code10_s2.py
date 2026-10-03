# EVAL_META: task_id=10, framework=qpanda, class=3
from pyqpanda3.core import *
def create_operator():
    circ = QCircuit()
    q = [0, 1]
    circ << X(q[0]) << X(q[1])
    return circ
