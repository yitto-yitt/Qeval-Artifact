# EVAL_META: task_id=5, framework=qpanda2, class=2
from pyqpanda import *


def create_state_prep():
    q0 = Qubit(0)
    q1 = Qubit(1)
    circuit = QCircuit()
    circuit << X(q0)
    return circuit
