# EVAL_META: task_id=109, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit, Parameter

def circuit():
    qc = QuantumCircuit(1)
    qc.h(0)
    theta = Parameter('th')
    qc.rz(theta, 0)
    return qc
