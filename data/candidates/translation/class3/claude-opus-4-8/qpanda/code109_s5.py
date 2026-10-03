# EVAL_META: task_id=109, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, RZ

def circuit():
    theta = "th"
    qc = QCircuit(1)
    qc << H(0)
    qc << RZ(0, theta)
    return qc
