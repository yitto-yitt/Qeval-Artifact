# EVAL_META: task_id=52, framework=qpanda2, class=1
from pyqpanda import QProg, Qubit, CBit, H, CNOT, X, Z, measure

def send_bits(bitstring):
    sender = Qubit(0)
    receiver = Qubit(1)
    c0 = CBit(0)
    c1 = CBit(1)
    prog = QProg()
    prog << H(sender) << CNOT(sender, receiver)
    if bitstring[1] == "1":
        prog << Z(sender)
    if bitstring[0] == "1":
        prog << X(sender)
    prog << CNOT(sender, receiver) << H(sender)
    prog << measure(sender, c0) << measure(receiver, c1)
    return prog
