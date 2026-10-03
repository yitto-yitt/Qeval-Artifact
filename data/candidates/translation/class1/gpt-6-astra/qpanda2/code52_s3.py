# EVAL_META: task_id=52, framework=qpanda2, class=1
import pyqpanda as pq


def send_bits(bitstring):
    machine = pq.CPUQVM()
    machine.init_qvm()
    sender, receiver = machine.qAlloc_many(2)
    measure = machine.cAlloc_many(2)

    program = pq.QProg()
    program << pq.H(sender)
    program << pq.CNOT(sender, receiver)

    if bitstring[1] == "1":
        program << pq.Z(sender)
    if bitstring[0] == "1":
        program << pq.X(sender)

    program << pq.CNOT(sender, receiver)
    program << pq.H(sender)
    program << pq.Measure(sender, measure[0])
    program << pq.Measure(receiver, measure[1])

    machine.run_with_configuration(program, measure, 1)

    if not hasattr(send_bits, "_machines"):
        send_bits._machines = []
    send_bits._machines.append(machine)
    return program
