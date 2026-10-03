# EVAL_META: task_id=52, framework=qpanda, class=1
from pyqpanda3.core import *


def send_bits(bitstring):
    circuit = QProg()
    cnot = globals().get("CNOT", globals().get("CX"))
    measure = globals().get("Measure", globals().get("measure"))

    circuit << H(0)
    circuit << cnot(0, 1)

    if bitstring[1] == "1":
        circuit << Z(0)
    if bitstring[0] == "1":
        circuit << X(0)

    circuit << cnot(0, 1)
    circuit << H(0)
    circuit << measure(0, 0)
    circuit << measure(1, 1)

    return circuit
