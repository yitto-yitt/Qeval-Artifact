# EVAL_META: task_id=52, framework=qpanda2, class=1
import pyqpanda as pq

_machines = []


def send_bits(bitstring):
    machine = pq.CPUQVM()
    machine.init_qvm()
    _machines.append(machine)
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)
    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1])
    if bitstring[1] == "1":
        prog << pq.Z(q[0])
    if bitstring[0] == "1":
        prog << pq.X(q[0])
    prog << pq.CNOT(q[0], q[1]) << pq.H(q[0])
    prog << pq.Measure(q[0], c[0]) << pq.Measure(q[1], c[1])
    return prog
