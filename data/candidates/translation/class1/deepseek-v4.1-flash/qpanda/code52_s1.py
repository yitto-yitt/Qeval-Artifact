# EVAL_META: task_id=52, framework=qpanda, class=1
from pyqpanda3.core import QProg, H, X, Z, CNOT, Measure


def send_bits(bitstring):
    prog = QProg()
    prog << H(0)
    prog << CNOT(0, 1)
    if bitstring[1] == "1":
        prog << Z(0)
    if bitstring[0] == "1":
        prog << X(0)
    prog << CNOT(0, 1)
    prog << H(0)
    prog << Measure(0, 0)
    prog << Measure(1, 1)
    return prog
