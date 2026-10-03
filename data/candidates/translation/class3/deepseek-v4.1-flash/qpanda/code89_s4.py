# EVAL_META: task_id=89, framework=qpanda, class=3
from pyqpanda3.core import *

def create_controlled_hgate():
    q = qAlloc_many(3)
    circuit = QCircuit()
    circuit << control(H(q[2]), [q[0], q[1]])
    return circuit
