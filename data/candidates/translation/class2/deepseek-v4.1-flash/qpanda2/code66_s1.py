# EVAL_META: task_id=66, framework=qpanda2, class=2
import numpy as np
from pyqpanda import *


def w_state():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(3)
    c = qvm.cAlloc_many(3)
    circuit = QCircuit()
    circuit << RY(q[0], 2 * np.arccos(1 / np.sqrt(3)))
    circuit << CH(q[0], q[1])
    circuit << CNOT(q[1], q[2])
    circuit << CNOT(q[0], q[1])
    circuit << X(q[0])
    circuit << measure(q[0], c[0])
    circuit << measure(q[1], c[1])
    circuit << measure(q[2], c[2])
    return circuit
