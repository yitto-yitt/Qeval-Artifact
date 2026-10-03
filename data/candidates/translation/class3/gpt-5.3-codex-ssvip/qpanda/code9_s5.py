# EVAL_META: task_id=9, framework=qpanda, class=3
from pyqpanda3.core import *

def create_efficientSU2():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(3)
    c = machine.cAlloc_many(3)

    prog = QProg()
    prog << RY(q[0], 0.0) << RZ(q[0], 0.0)
    prog << RY(q[1], 0.0) << RZ(q[1], 0.0)
    prog << RY(q[2], 0.0) << RZ(q[2], 0.0)

    prog << BARRIER(q)

    prog << CNOT(q[0], q[1])
    prog << CNOT(q[1], q[2])

    prog << BARRIER(q)

    prog << RY(q[0], 0.0) << RZ(q[0], 0.0)
    prog << RY(q[1], 0.0) << RZ(q[1], 0.0)
    prog << RY(q[2], 0.0) << RZ(q[2], 0.0)

    return prog
