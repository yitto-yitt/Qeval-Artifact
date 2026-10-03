# EVAL_META: task_id=52, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, X, Z, Measure


def send_bits(bitstring):
    qvm = CPUQVM()
    qvm.init_qvm()
    sender = qvm.qAlloc_many(1)[0]
    receiver = qvm.qAlloc_many(1)[0]
    cbits = qvm.cAlloc_many(2)
    prog = QProg()
    prog << H(sender) << CNOT(sender, receiver)
    if bitstring[1] == "1":
        prog << Z(sender)
    if bitstring[0] == "1":
        prog << X(sender)
    prog << CNOT(sender, receiver) << H(sender)
    prog << Measure(sender, cbits[0]) << Measure(receiver, cbits[1])
    return prog
