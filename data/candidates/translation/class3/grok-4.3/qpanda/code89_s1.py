# EVAL_META: task_id=89, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, qAlloc_many, H

def create_controlled_hgate():
    qr = qAlloc_many(3)
    qc = QCircuit()
    c3h_gate = H(qr[2]).control([qr[0], qr[1]])
    qc << c3h_gate
    return qc
