# EVAL_META: task_id=52, framework=qpanda2, class=1
import pyqpanda as pq


def send_bits(bitstring):
    machine = pq.CPUQVM()
    machine.init_qvm()

    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)

    prog = pq.QProg()
    prog.insert(pq.H(q[0]))
    prog.insert(pq.CNOT(q[0], q[1]))

    if bitstring[1] == "1":
        prog.insert(pq.Z(q[0]))
    if bitstring[0] == "1":
        prog.insert(pq.X(q[0]))

    prog.insert(pq.CNOT(q[0], q[1]))
    prog.insert(pq.H(q[0]))
    prog.insert(pq.Measure(q[0], c[0]))
    prog.insert(pq.Measure(q[1], c[1]))

    if not hasattr(send_bits, "_machines"):
        send_bits._machines = []
    send_bits._machines.append(machine)

    return prog
