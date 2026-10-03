# EVAL_META: task_id=52, framework=qpanda2, class=1
import pyqpanda as pq


def send_bits(bitstring):
    machine = pq.CPUQVM()
    machine.init_qvm()

    qubits = machine.qAlloc_many(2)
    cbits = machine.cAlloc_many(2)

    sender = qubits[0]
    receiver = qubits[1]

    prog = pq.QProg()
    prog << pq.H(sender)
    prog << pq.CNOT(sender, receiver)

    if bitstring[1] == "1":
        prog << pq.Z(sender)
    if bitstring[0] == "1":
        prog << pq.X(sender)

    prog << pq.CNOT(sender, receiver)
    prog << pq.H(sender)
    prog << pq.Measure(sender, cbits[0])
    prog << pq.Measure(receiver, cbits[1])

    if not hasattr(send_bits, "_resources"):
        send_bits._resources = []
    send_bits._resources.append((machine, qubits, cbits))

    return prog
