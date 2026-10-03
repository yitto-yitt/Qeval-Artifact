# EVAL_META: task_id=67, framework=qpanda2, class=1
from numpy import pi
import pyqpanda as pq


def chsh_circuit(alice, bob):
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
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
    return prog
