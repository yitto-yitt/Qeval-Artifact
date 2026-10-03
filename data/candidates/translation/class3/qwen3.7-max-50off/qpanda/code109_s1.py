# EVAL_META: task_id=109, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Qubit, H, RZ, Parameter

def circuit():
    qc = QCircuit()
    q = Qubit()
    qc << H(q)
    theta = Parameter('th')
    qc << RZ(q, theta)
    return qc
