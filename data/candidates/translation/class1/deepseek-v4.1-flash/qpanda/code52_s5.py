# EVAL_META: task_id=52, framework=qpanda, class=1
from pyqpanda3.core import QCircuit, Qubit, CBit, H, X, Z, CNOT, Measure, BARRIER

def send_bits(bitstring):
    sender = Qubit(0)
    receiver = Qubit(1)
    measure = [CBit(0), CBit(1)]
    circuit = QCircuit()
    circuit << H(sender)
    circuit << CNOT(sender, receiver)
    circuit << BARRIER([sender, receiver])
    if bitstring[1] == "1":
        circuit << Z(sender)
    if bitstring[0] == "1":
        circuit << X(sender)
    circuit << BARRIER([sender, receiver])
    circuit << CNOT(sender, receiver)
    circuit << H(sender)
    circuit << Measure(sender, measure[0])
    circuit << Measure(receiver, measure[1])
    return circuit
