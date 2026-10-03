# EVAL_META: task_id=67, framework=qpanda, class=1
import numpy as np
import pyqpanda3.core as pq


def chsh_circuit(alice, bob):
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)

    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1])

    if alice == 0:
        prog << pq.RY(q[0], 0.0)
    else:
        prog << pq.RY(q[0], -np.pi / 2)

    prog << pq.Measure(q[0], c[0])

    if bob == 0:
        prog << pq.RY(q[1], -np.pi / 4)
    else:
        prog << pq.RY(q[1], np.pi / 4)

    prog << pq.Measure(q[1], c[1])

    # Bind the machine to the program to prevent garbage collection
    prog.machine = machine
    return prog
