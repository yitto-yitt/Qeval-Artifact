# EVAL_META: task_id=89, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H

def create_controlled_hgate():
    qc = QCircuit()
    h_gate = H(2)
    controlled_h = h_gate.control([0, 1])
    qc << controlled_h
    return qc
