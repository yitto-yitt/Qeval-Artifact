# EVAL_META: task_id=23, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, X

def dj_constant_oracle():
    oracle = QCircuit()
    oracle.insert(X(2))
    return oracle
