# EVAL_META: task_id=52, framework=qpanda2, class=1
from pyqpanda import *


def send_bits(bitstring):
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)
    c = qvm.cAlloc_many(2)

    prog = QProg()
    prog << H(q[0])
    prog << CNOT(q[0], q[1])

    if bitstring[1] == "1":
        prog << Z(q[0])
    if bitstring[0] == "1":
        prog << X(q[0])

    prog << CNOT(q[0], q[1])
    prog << H(q[0])
    prog << Measure(q[0], c[0])
    prog << Measure(q[1], c[1])

    return prog
