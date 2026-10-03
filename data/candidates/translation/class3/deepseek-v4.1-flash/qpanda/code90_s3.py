# EVAL_META: task_id=90, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, X, H, control

def create_custom_controlled():
    qc = QCircuit(4)
    qc << control(X(1), [0, 3])
    qc << control(H(2), [0, 3])
    return qc
