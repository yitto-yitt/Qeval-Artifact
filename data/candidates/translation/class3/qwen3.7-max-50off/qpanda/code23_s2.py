# EVAL_META: task_id=23, framework=qpanda, class=3
from pyqpanda3.core import QMachine, QCircuit, X

def dj_constant_oracle():
    qm = QMachine()
    q = qm.qAlloc_many(3)
    oracle = QCircuit()
    oracle << X(q[2])
    return oracle
