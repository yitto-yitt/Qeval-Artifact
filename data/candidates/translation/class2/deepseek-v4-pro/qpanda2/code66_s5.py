# EVAL_META: task_id=66, framework=qpanda2, class=2
from numpy import arccos, sqrt
from pyqpanda import *


def w_state():
    init(QMachineType.CPU)
    q = qAlloc_many(3)
    c = cAlloc_many(3)

    circuit = QProg()
    circuit << RY(q[0], 2 * arccos(1 / sqrt(3)))
    circuit << CH(q[0], q[1])
    circuit << CNOT(q[1], q[2])
    circuit << CNOT(q[0], q[1])
    circuit << X(q[0])
    circuit << Measure(q[0], c[0])
    circuit << Measure(q[1], c[1])
    circuit << Measure(q[2], c[2])

    return circuit
