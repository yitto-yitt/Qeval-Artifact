# EVAL_META: task_id=10, framework=qpanda, class=3
from pyqpanda3.core import init, qAlloc_many, QCircuit, X

def create_operator():
    init()
    q = qAlloc_many(2)
    circuit = QCircuit()
    circuit << X(q[0]) << X(q[1])
    return circuit
