# EVAL_META: task_id=52, framework=qpanda2, class=1
import pyqpanda as pq


def send_bits(bitstring):
    pq.init(pq.QMachineType.CPU)
    qubits = pq.qAlloc_many(2)
    cbits = pq.cAlloc_many(2)

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

    return prog
