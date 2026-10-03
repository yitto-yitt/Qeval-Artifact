# EVAL_META: task_id=89, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H

def create_controlled_hgate():
    circuit = QCircuit()
    circuit << H(2).control([0, 1])
    return circuit
