# EVAL_META: task_id=9, framework=qpanda, class=3
from pyqpanda3.core import *

def create_efficientSU2():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(3)

    prog = QProg()

    for i in range(3):
        prog << RY(q[i], 0.0)
    prog << BARRIER(q)
    for i in range(3):
        prog << RZ(q[i], 0.0)
    prog << BARRIER(q)

    prog << CNOT(q[0], q[1]) << CNOT(q[1], q[2])
    prog << BARRIER(q)

    for i in range(3):
        prog << RY(q[i], 0.0)
    prog << BARRIER(q)
    for i in range(3):
        prog << RZ(q[i], 0.0)

    return prog
