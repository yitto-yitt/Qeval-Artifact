# EVAL_META: task_id=52, framework=qpanda2, class=1
from pyqpanda import *


def send_bits(bitstring):
    init(QMachineType.CPU)
    sender = qAlloc()
    receiver = qAlloc()
    measure = cAlloc_many(2)

    prog = QProg()
    prog << H(sender) << CNOT(sender, receiver)

    if bitstring[1] == "1":
        prog << Z(sender)
    if bitstring[0] == "1":
        prog << X(sender)

    prog << CNOT(sender, receiver) << H(sender)
    prog << Measure(sender, measure[0]) << Measure(receiver, measure[1])

    return prog
