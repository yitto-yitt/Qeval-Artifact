# EVAL_META: task_id=59, framework=qpanda, class=3
from pyqpanda3.core import *

def create_cz_gate():
    circuit = QCircuit()
    q = qAlloc_many(2)
    circuit << H(q[1]) << CNOT(q[0], q[1]) << H(q[1])
    return circuit
