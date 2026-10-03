# EVAL_META: task_id=5, framework=qpanda, class=2
from pyqpanda3.core import QCircuit, qAlloc, X

def create_state_prep():
    q = qAlloc(2)
    qc = QCircuit()
    qc << X(q[0])
    return qc
