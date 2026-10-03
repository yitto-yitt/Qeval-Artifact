# EVAL_META: task_id=109, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, RZ, Var

def circuit():
    qc = QCircuit()
    qc << H(0)
    theta = Var('th')
    qc << RZ(0, theta)
    return qc
