# EVAL_META: task_id=49, framework=qpanda, class=3
from pyqpanda3.core import *

def simple_elitzur_vaidman():
    circuit = QCircuit()
    q = qAlloc_many(2)
    circuit << H(q[0]) << CNOT(q[0], q[1]) << H(q[0])
    return circuit
