# EVAL_META: task_id=89, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H

def create_controlled_hgate():
    qc = QCircuit()
    q = qc.qAlloc(3)
    c3h_gate = H(q[2]).control([q[0], q[1]])
    qc << c3h_gate
    return qc
