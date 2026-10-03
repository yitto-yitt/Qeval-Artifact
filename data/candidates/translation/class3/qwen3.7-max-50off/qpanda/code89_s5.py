# EVAL_META: task_id=89, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, QVec

def create_controlled_hgate():
    q = QVec(3)
    qc = QCircuit()
    qc << H(q[2]).control([q[0], q[1]])
    return qc
