# EVAL_META: task_id=52, framework=qpanda, class=1
from pyqpanda3.core import QCircuit, H, CNOT, X, Z, Measure, qAlloc_many, cAlloc_many

def send_bits(bitstring):
    q = qAlloc_many(2)
    c = cAlloc_many(2)
    sender = q[0]
    receiver = q[1]
    measure0 = c[0]
    measure1 = c[1]

    circuit = QCircuit()
    circuit << H(sender) << CNOT(sender, receiver)
    if bitstring[1] == '1':
        circuit << Z(sender)
    if bitstring[0] == '1':
        circuit << X(sender)
    circuit << CNOT(sender, receiver) << H(sender)
    circuit << Measure(sender, measure0) << Measure(receiver, measure1)
    return circuit
