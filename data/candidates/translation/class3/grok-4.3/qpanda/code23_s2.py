# EVAL_META: task_id=23, framework=qpanda, class=3
from pyqpanda3.core import QuantumMachine, QCircuit, X

def dj_constant_oracle():
    qvm = QuantumMachine()
    q = qvm.qAlloc_many(3)
    oracle = QCircuit()
    oracle << X(q[2])
    return oracle
