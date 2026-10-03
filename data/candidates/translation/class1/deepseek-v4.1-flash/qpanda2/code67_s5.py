# EVAL_META: task_id=67, framework=qpanda2, class=1
from pyqpanda import *
from numpy import pi

def chsh_circuit(alice, bob):
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)
    c = qvm.cAlloc_many(2)
    prog = QProg()
    prog << H(q[0])
    prog << CNOT(q[0], q[1])
    prog << BARRIER(q)
    if alice == 0:
        prog << RY(q[0], 0)
    else:
        prog << RY(q[0], -pi / 2)
    prog << measure(q[0], c[0])
    if bob == 0:
        prog << RY(q[1], -pi / 4)
    else:
        prog << RY(q[1], pi / 4)
    prog << measure(q[1], c[1])
    return prog
