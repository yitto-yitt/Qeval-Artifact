# EVAL_META: task_id=89, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, H

def create_controlled_hgate():
    qc = QCircuit()
    h_gate = H(2)
    h_gate = h_gate.control([0, 1])
    qc << h_gate
    return qc
