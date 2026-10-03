# EVAL_META: task_id=109, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit, H, RZ, Parameter

def circuit():
    qc = QuantumCircuit()
    q = qc.qalloc()
    theta = Parameter('th', 0.0)
    qc << H(q)
    qc << RZ(q, theta)
    return qc
