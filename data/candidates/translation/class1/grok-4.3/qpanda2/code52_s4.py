# EVAL_META: task_id=52, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def send_bits(bitstring):
    qvm = CPUQVM()
    qvm.init_qvm()
    sender = qvm.qAlloc()
    receiver = qvm.qAlloc()
    cbits = qvm.cAlloc_many(2)
    prog = QProg()
    prog << H(sender) << CNOT(sender, receiver)
    if bitstring[1] == "1":
        prog << Z(sender)
    if bitstring[0] == "1":
        prog << X(sender)
    prog << CNOT(sender, receiver) << H(sender)
    prog << Measure(sender, cbits[0]) << Measure(receiver, cbits[1])
    shots = 1024
    result = qvm.run_with_configuration(prog, cbits, shots)
    return result
