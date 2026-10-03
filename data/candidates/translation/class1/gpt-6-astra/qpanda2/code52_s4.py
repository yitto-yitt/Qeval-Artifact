# EVAL_META: task_id=52, framework=qpanda2, class=1
from pyqpanda import CPUQVM, QProg, H, CNOT, Z, X, Measure


def send_bits(bitstring):
    machine = CPUQVM()
    machine.init_qvm()
    sender, receiver = machine.qAlloc_many(2)
    measure = machine.cAlloc_many(2)

    program = QProg()
    program << H(sender) << CNOT(sender, receiver)

    if bitstring[1] == "1":
        program << Z(sender)
    if bitstring[0] == "1":
        program << X(sender)

    program << CNOT(sender, receiver) << H(sender)
    program << Measure(sender, measure[0])
    program << Measure(receiver, measure[1])

    machine.directly_run(program)

    if not hasattr(send_bits, "_machines"):
        send_bits._machines = []
    send_bits._machines.append(machine)

    return program
