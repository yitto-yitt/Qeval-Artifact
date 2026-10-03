# EVAL_META: task_id=52, framework=qpanda2, class=1
import pyqpanda as pq


def send_bits(bitstring):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qubit_alloc_many(2)
    cbits = machine.cbit_alloc_many(2)
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

    prog << pq.measure(sender, cbits[0])
    prog << pq.measure(receiver, cbits[1])

    shots = 1024
    result = machine.run_with_configuration(prog, cbits, shots)

    machine.finalize()
    return result
