# EVAL_META: task_id=52, framework=qpanda2, class=1
from pyqpanda import *


def send_bits(bitstring):
    sender = qAlloc_many(1)
    receiver = qAlloc_many(1)
    measure = cAlloc_many(2)

    circuit = QProg()
    circuit << H(sender[0]) << CNOT(sender[0], receiver[0])

    if bitstring[1] == "1":
        circuit << Z(sender[0])
    if bitstring[0] == "1":
        circuit << X(sender[0])

    circuit << CNOT(sender[0], receiver[0]) << H(sender[0])
    circuit << Measure(sender[0], measure[0]) << Measure(receiver[0], measure[1])

    return circuit
