# EVAL_META: task_id=23, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, X

def dj_constant_oracle():
    qubits = list(range(3))
    oracle = QCircuit()
    oracle << X(qubits[2])
    return oracle
