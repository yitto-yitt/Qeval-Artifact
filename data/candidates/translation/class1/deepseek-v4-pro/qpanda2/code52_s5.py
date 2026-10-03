# EVAL_META: task_id=52, framework=qpanda2, class=1
from pyqpanda import *

def send_bits(bitstring):
    qvm = CPUQVM()
    qvm.init_qvm()
    sender, receiver = qvm.qAlloc_many(2)
    measure = qvm.cAlloc_many(2)

    circuit = QCircuit()
    circuit << H(sender) << CNOT(sender, receiver)

    if bitstring[1] == "1":
        circuit << Z(sender)
    if bitstring[0] == "1":
        circuit << X(sender)

    circuit << CNOT(sender, receiver) << H(sender)
    circuit << Measure(sender, measure[0]) << Measure(receiver, measure[1])

    return circuit
