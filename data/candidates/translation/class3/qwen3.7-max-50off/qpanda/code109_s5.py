# EVAL_META: task_id=109, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Parameter, H, RZ

def circuit():
    qc = QCircuit()
    q = qc[0]
    qc << H(q)
    theta = Parameter('th')
    qc << RZ(q, theta)
    return qc
