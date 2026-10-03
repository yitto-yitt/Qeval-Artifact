# EVAL_META: task_id=109, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Qubit, H, RZ, Parameter

def circuit():
    q = Qubit(0)
    c = QCircuit()
    c << H(q)
    theta = Parameter('th')
    c << RZ(q, theta)
    return c
