# EVAL_META: task_id=67, framework=qpanda, class=1
from math import pi
from pyqpanda3.core import *

def chsh_circuit(alice, bob):
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)
    c = qvm.cAlloc_many(2)

    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])

    if alice == 0:
        prog << RY(q[0], 0.0)
    else:
        prog << RY(q[0], -pi / 2)

    prog << Measure(q[0], c[0])

    if bob == 0:
        prog << RY(q[1], -pi / 4)
    else:
        prog << RY(q[1], pi / 4)

    prog << Measure(q[1], c[1])
    return prog
