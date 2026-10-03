# EVAL_META: task_id=52, framework=qpanda, class=1
from pyqpanda3.core import QCircuit, QProg, H, CNOT, X, Z, measure


def send_bits(bitstring):
    sender = 0
    receiver = 1
    prog = QProg()
    prog << H(sender)
    prog << CNOT(sender, receiver)
    if bitstring[1] == "1":
        prog << Z(sender)
    if bitstring[0] == "1":
        prog << X(sender)
    prog << CNOT(sender, receiver)
    prog << H(sender)
    prog << measure(sender, 0)
    prog << measure(receiver, 1)
    return prog
