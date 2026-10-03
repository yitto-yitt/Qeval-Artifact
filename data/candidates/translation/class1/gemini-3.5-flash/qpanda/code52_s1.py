# EVAL_META: task_id=52, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, X, Z, Measure, BARRIER


def send_bits(bitstring):
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)
    prog = QProg()

    prog << H(q[0])
    prog << CNOT(q[0], q[1])
    prog << BARRIER(q)

    if bitstring[1] == "1":
        prog << Z(q[0])
    if bitstring[0] == "1":
        prog << X(q[0])

    prog << BARRIER(q)
    prog << CNOT(q[0], q[1])
    prog << H(q[0])
    prog << Measure(q[0], c[0])
    prog << Measure(q[1], c[1])

    return prog
