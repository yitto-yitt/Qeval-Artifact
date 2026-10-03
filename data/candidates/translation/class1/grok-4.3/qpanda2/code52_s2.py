# EVAL_META: task_id=52, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def send_bits(bitstring):
    machine = init_quantum_machine(QMachineType.CPU)
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)
    sender = q[0]
    receiver = q[1]
    prog = QProg()
    prog << H(sender) << CNOT(sender, receiver)
    if bitstring[1] == "1":
        prog << Z(sender)
    if bitstring[0] == "1":
        prog << X(sender)
    prog << CNOT(sender, receiver) << H(sender)
    prog << Measure(sender, c[0]) << Measure(receiver, c[1])
    shots = 1024
    result = machine.run_with_configuration(prog, c, shots)
    return result
