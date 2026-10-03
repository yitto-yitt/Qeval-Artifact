# EVAL_META: task_id=109, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, RZ, AllocateQubit, var

def circuit():
    qc = QCircuit()
    q = AllocateQubit()
    theta = var(0.0)
    qc << H(q)
    qc << RZ(q, theta)
    return qc
