# EVAL_META: task_id=66, framework=qpanda2, class=2
from numpy import arccos, sqrt
from pyqpanda import *

def w_state():
    init_quantum_machine(QMachineType.CPU)
    q = qAlloc_many(3)
    c = cAlloc_many(3)
    prog = QProg()
    theta = 2 * arccos(1 / sqrt(3))
    prog << RY(q[0], theta)
    # Controlled-H decomposition: S H T CNOT Tdag H Sdag
    prog << S(q[1])
    prog << H(q[1])
    prog << T(q[1])
    prog << CNOT(q[0], q[1])
    prog << Tdag(q[1])
    prog << H(q[1])
    prog << Sdag(q[1])
    prog << CNOT(q[1], q[2])
    prog << CNOT(q[0], q[1])
    prog << X(q[0])
    for i in range(3):
        prog << Measure(q[i], c[i])
    return prog
