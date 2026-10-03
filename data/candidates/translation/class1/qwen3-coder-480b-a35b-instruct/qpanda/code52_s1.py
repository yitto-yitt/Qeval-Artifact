# EVAL_META: task_id=52, framework=qpanda, class=1
from pyqpanda import *


def send_bits(bitstring):
    machine = init(QMachineType.CPU)
    sender = machine.qAlloc_many(1)
    receiver = machine.qAlloc_many(1)
    measure = machine.cAlloc_many(2)
    prog = QProg()
    prog.insert(H(sender[0]))
    prog.insert(CNOT(sender[0], receiver[0]))
    prog.insert(BARRIER(machine.qAlloc_many(2)))
    if bitstring[1] == "1":
        prog.insert(Z(sender[0]))
    if bitstring[0] == "1":
        prog.insert(X(sender[0]))
    prog.insert(BARRIER(machine.qAlloc_many(2)))
    prog.insert(CNOT(sender[0], receiver[0]))
    prog.insert(H(sender[0]))
    prog.insert(Measure(sender[0], measure[0]))
    prog.insert(Measure(receiver[0], measure[1]))
    return prog
