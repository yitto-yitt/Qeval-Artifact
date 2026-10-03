# EVAL_META: task_id=5, framework=qpanda, class=2
from pyqpanda3.core import QCircuit, X


def create_state_prep():
    qc = QCircuit(2)
    qc << X(1)
    return qc
