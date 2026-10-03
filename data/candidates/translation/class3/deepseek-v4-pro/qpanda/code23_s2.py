# EVAL_META: task_id=23, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit

def dj_constant_oracle():
    oracle = QuantumCircuit(3)
    oracle.x(2)
    return oracle
