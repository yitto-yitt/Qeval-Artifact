# EVAL_META: task_id=67, framework=qpanda2, class=1
from math import pi
import pyqpanda as pq


def chsh_circuit(alice, bob):
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)

    prog = pq.QProg()
    prog.insert(pq.H(q[0]))
    prog.insert(pq.CNOT(q[0], q[1]))
    prog.insert(pq.BARRIER(q))

    if alice == 0:
        prog.insert(pq.RY(q[0], 0.0))
    else:
        prog.insert(pq.RY(q[0], -pi / 2))
    prog.insert(pq.Measure(q[0], c[0]))

    if bob == 0:
        prog.insert(pq.RY(q[1], -pi / 4))
    else:
        prog.insert(pq.RY(q[1], pi / 4))
    prog.insert(pq.Measure(q[1], c[1]))

    return prog
