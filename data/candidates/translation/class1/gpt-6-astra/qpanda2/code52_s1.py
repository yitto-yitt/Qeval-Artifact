# EVAL_META: task_id=52, framework=qpanda2, class=1
from pyqpanda import CPUQVM, QProg, H, CNOT, Z, X, Measure


def send_bits(bitstring):
    machine = CPUQVM()
    machine.init_qvm()
    sender, receiver = machine.qAlloc_many(2)
    measure = machine.cAlloc_many(2)

    circuit = QProg()
    circuit << H(sender)
    circuit << CNOT(sender, receiver)

    if bitstring[1] == "1":
        circuit << Z(sender)
    if bitstring[0] == "1":
        circuit << X(sender)

    circuit << CNOT(sender, receiver)
    circuit << H(sender)
    circuit << Measure(sender, measure[0])
    circuit << Measure(receiver, measure[1])

    machine.run_with_configuration(circuit, measure, 1)

    if not hasattr(send_bits, "_machines"):
        send_bits._machines = []
    send_bits._machines.append(machine)

    return circuit
