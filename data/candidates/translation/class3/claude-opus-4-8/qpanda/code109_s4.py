# EVAL_META: task_id=109, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, H, RZ

def circuit(theta):
    qc = QCircuit(1)
    qc << H(0)
    qc << RZ(0, theta)
    prog = QProg()
    prog << qc
    return prog
