# EVAL_META: task_id=5, framework=qpanda, class=2
from pyqpanda3.core import QCircuit, X, qAllocMany


def create_state_prep():
    q = qAllocMany(2)
    circuit = QCircuit()
    circuit << X(q[0])
    return circuit
