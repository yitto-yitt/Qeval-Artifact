# EVAL_META: task_id=109, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Parameter, H, RZ

def circuit():
    qc = QCircuit()
    theta = Parameter('th')
    qc << H(0) << RZ(0, theta)
    return qc
