# EVAL_META: task_id=23, framework=qpanda, class=3
from pyqpanda3.core import QMachine, QCircuit

def dj_constant_oracle():
    qm = QMachine()
    q = qm.alloc(3)
    oracle = QCircuit()
    oracle.x(q[2])
    return oracle
