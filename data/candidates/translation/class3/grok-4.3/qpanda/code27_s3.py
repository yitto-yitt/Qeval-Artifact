# EVAL_META: task_id=27, framework=qpanda, class=3
from pyqpanda3.core import *

def apply_op_back():
    qm = QuantumMachine()
    q = qm.qAlloc_many(3)
    c = qm.cAlloc_many(3)
    circ = QCircuit()
    circ << H(q[0]) << CNOT(q[0], q[1])
    circ << H(q[0])
    return circ
