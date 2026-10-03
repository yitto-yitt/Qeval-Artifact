# EVAL_META: task_id=23, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, X, Qubit

def dj_constant_oracle():
    oracle = QCircuit()
    q = [Qubit(i) for i in range(3)]
    oracle << X(q[2])
    return oracle
