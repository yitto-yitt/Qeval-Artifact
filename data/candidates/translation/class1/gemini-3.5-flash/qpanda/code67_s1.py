# EVAL_META: task_id=67, framework=qpanda, class=1
import pyqpanda3.core as pq
from numpy import pi

_machines = []


def chsh_circuit(alice, bob):
    machine = pq.CPUQVM()
    machine.init_qvm()
    _machines.append(machine)

    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)

    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1]) << pq.BARRIER(q)

    if alice == 0:
        prog << pq.RY(q[0], 0.0)
    else:
        prog << pq.RY(q[0], -pi / 2)

    prog << pq.Measure(q[0], c[0])

    if bob == 0:
        prog << pq.RY(q[1], -pi / 4)
    else:
        prog << pq.RY(q[1], pi / 4)

    prog << pq.Measure(q[1], c[1])

    # Keep machine alive by attaching it to the returned program
    prog.machine = machine

    return prog
