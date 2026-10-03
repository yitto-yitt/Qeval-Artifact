# EVAL_META: task_id=52, framework=qpanda, class=1
from pyqpanda3.core import QCircuit, Qubit, CBit, H, X, Z, CNOT, Measure


def send_bits(bitstring):
    sender = Qubit(0)
    receiver = Qubit(1)
    c0 = CBit(0)
    c1 = CBit(1)
    circuit = QCircuit()
    circuit << H(sender)
    circuit << CNOT(sender, receiver)
    if bitstring[1] == "1":
        circuit << Z(sender)
    if bitstring[0] == "1":
        circuit << X(sender)
    circuit << CNOT(sender, receiver)
    circuit << H(sender)
    circuit << Measure(sender, c0)
    circuit << Measure(receiver, c1)
    return circuit
