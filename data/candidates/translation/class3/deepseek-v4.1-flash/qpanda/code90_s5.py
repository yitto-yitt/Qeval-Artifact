# EVAL_META: task_id=90, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, X, H

def create_custom_controlled():
    custom = QCircuit()
    custom << X(1) << H(2)
    return custom.control([0, 3])
