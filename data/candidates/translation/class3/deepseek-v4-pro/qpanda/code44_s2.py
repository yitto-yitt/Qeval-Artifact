# EVAL_META: task_id=44, framework=qpanda, class=3
from pyqpanda3.core import Allocate, CR, QCircuit, X, init

def tensor_circuits():
    init()
    q = Allocate(3)
    circ = QCircuit()
    circ << CR(q[0], q[1], 0.2)
    circ << X(q[2])
    return circ
