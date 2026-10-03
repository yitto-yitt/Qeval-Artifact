# EVAL_META: task_id=52, framework=qpanda2, class=1
from pyqpanda import *

def send_bits(bitstring):
    qubits = qAlloc_many(2)
    sender = qubits[0]
    receiver = qubits[1]
    cbits = cAlloc_many(2)

    prog = QProg()
    prog << H(sender) << CNOT(sender, receiver)

    if bitstring[1] == "1":
        prog << Z(sender)
    if bitstring[0] == "1":
        prog << X(sender)

    prog << CNOT(sender, receiver) << H(sender)
    prog << measure(sender, cbits[0]) << measure(receiver, cbits[1])

    return prog
