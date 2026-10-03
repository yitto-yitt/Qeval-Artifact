# EVAL_META: task_id=49, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CNOT

def simple_elitzur_vaidman():
    qc = QCircuit()
    qc << H(0)
    qc << CNOT(0, 1)
    qc << H(0)
    return qc
