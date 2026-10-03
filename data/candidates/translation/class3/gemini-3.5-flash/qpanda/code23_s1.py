# EVAL_META: task_id=23, framework=qpanda, class=3
from pyqpanda3.core import *

def dj_constant_oracle():
    qubits = qAlloc_many(3)
    circuit = QCircuit()
    circuit << X(qubits[2])
    return circuit
