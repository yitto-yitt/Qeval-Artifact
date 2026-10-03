# EVAL_META: task_id=52, framework=qpanda, class=1
import pyqpanda3.core as pq


def send_bits(bitstring):
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.q_alloc_many(2)
    c = machine.c_alloc_many(2)

    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1])

    if bitstring[1] == "1":
        prog << pq.Z(q[0])
    if bitstring[0] == "1":
        prog << pq.X(q[0])

    prog << pq.CNOT(q[0], q[1]) << pq.H(q[0]) << pq.Measure(
        q[0], c[0]
    ) << pq.Measure(q[1], c[1])

    prog.machine = machine
    return prog
