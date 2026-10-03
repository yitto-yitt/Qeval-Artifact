# EVAL_META: task_id=52, framework=qpanda2, class=1
from pyqpanda import *


def send_bits(bitstring):
    q0 = Qubit(0)
    q1 = Qubit(1)
    c0 = CBit(0)
    c1 = CBit(1)

    prog = QProg()
    prog << H(q0)
    prog << CNOT(q0, q1)

    if bitstring[1] == "1":
        prog << Z(q0)
    if bitstring[0] == "1":
        prog << X(q0)

    prog << CNOT(q0, q1)
    prog << H(q0)

    prog << Measure(q0, c0)
    prog << Measure(q1, c1)

    return prog
