# EVAL_META: task_id=5, framework=qpanda2, class=2
from pyqpanda import *


def create_state_prep():
    init(QMachineType.CPU)
    q = qAlloc_many(2)
    circuit = QCircuit()
    circuit << X(q[1])
    return circuit
