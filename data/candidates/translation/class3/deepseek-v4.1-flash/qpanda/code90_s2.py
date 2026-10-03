# EVAL_META: task_id=90, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, X, H

def create_custom_controlled():
    circuit = QCircuit()
    circuit << X(1).control([0, 3])
    circuit << H(2).control([0, 3])
    return circuit
