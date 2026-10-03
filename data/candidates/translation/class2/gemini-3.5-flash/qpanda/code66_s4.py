# EVAL_META: task_id=66, framework=qpanda, class=2
import numpy as np
import pyqpanda3.core as pq


def w_state():
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(3)
    c = machine.cAlloc_many(3)

    prog = pq.QProg()

    theta = 2 * np.arccos(1 / np.sqrt(3))
    prog << pq.RY(q[0], theta)
    prog << pq.H(q[1]).control([q[0]])
    prog << pq.CNOT(q[1], q[2])
    prog << pq.CNOT(q[0], q[1])
    prog << pq.X(q[0])

    for i in range(3):
        prog << pq.Measure(q[i], c[i])

    return prog
