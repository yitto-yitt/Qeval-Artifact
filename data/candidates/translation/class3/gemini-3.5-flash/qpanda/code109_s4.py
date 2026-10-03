# EVAL_META: task_id=109, framework=qpanda, class=3
from pyqpanda3.core import *

machine = CPUQVM()
machine.init_qvm()

def circuit():
    q = machine.qAlloc()
    qc = QCircuit()
    qc << H(q)
    theta = var(0.0)
    qc << RZ(q, theta)
    return qc
