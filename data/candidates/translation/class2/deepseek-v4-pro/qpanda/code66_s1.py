# EVAL_META: task_id=66, framework=qpanda, class=2
from pyqpanda3 import *
import math


def w_state():
    num_qubits = 3
    q = qAlloc_many(num_qubits)
    c = cAlloc_many(num_qubits)
    prog = QProg()
    theta = 2 * math.acos(1 / math.sqrt(3))
    prog << RY(q[0], theta)
    # ch(0, 1) decomposition: CZ then RY(pi/2) on target
    prog << CZ(q[0], q[1]) << RY(q[1], math.pi / 2)
    prog << CNOT(q[1], q[2])
    prog << CNOT(q[0], q[1])
    prog << X(q[0])
    # measure all qubits
    for i in range(num_qubits):
        prog << Measure(q[i], c[i])
    return prog
