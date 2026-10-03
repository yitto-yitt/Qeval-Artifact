# EVAL_META: task_id=89, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H

def create_controlled_hgate():
    qc = QCircuit(3)
    h_gate = H(2)
    c3h_gate = h_gate.control([0, 1])
    qc << c3h_gate
    return qc
