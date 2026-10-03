# EVAL_META: task_id=52, framework=qpanda2, class=1
from pyqpanda import *

def send_bits(bitstring):
    qvm = CPUQVM()
    qvm.init_qvm()
    sender = qvm.qAlloc_many(1)
    receiver = qvm.qAlloc_many(1)
    c = qvm.cAlloc_many(2)
    prog = QProg()
    prog << H(sender[0]) << CNOT(sender[0], receiver[0])
    if bitstring[1] == "1":
        prog << Z(sender[0])
    if bitstring[0] == "1":
        prog << X(sender[0])
    prog << CNOT(sender[0], receiver[0]) << H(sender[0])
    prog << Measure(sender[0], c[0])
    prog << Measure(receiver[0], c[1])
    return prog
