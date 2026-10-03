# EVAL_META: task_id=109, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Qubit, H, RZ, Var

def circuit():
    q = Qubit(0)
    theta = Var(0)
    circ = QCircuit()
    circ << H(q)
    circ << RZ(q, theta)
    return circ
