# EVAL_META: task_id=52, framework=qpanda, class=1
from pyqpanda3.core import QCircuit, QProg, H, CNOT, X, Z, measure


def send_bits(bitstring):
    sender = 0
    receiver = 1
    circuit = QCircuit()
    circuit << H(sender)
    circuit << CNOT(sender, receiver)
    if bitstring[1] == "1":
        circuit << Z(sender)
    if bitstring[0] == "1":
        circuit << X(sender)
    circuit << CNOT(sender, receiver)
    circuit << H(sender)
    prog = QProg()
    prog << circuit
    prog << measure(sender, 0)
    prog << measure(receiver, 1)
    return prog
