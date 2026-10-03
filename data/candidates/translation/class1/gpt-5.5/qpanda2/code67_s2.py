# EVAL_META: task_id=67, framework=qpanda2, class=1
from numpy import pi
from pyqpanda import *


def chsh_circuit(alice, bob):
    if not hasattr(chsh_circuit, "_qvm"):
        chsh_circuit._qvm = CPUQVM()
        chsh_circuit._qvm.init_qvm()

    qvm = chsh_circuit._qvm
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
    prog << Measure(q[0], c[0])

    if bob == 0:
        prog << RY(q[1], -pi / 4)
    else:
        prog << RY(q[1], pi / 4)
    prog << Measure(q[1], c[1])

    chsh_circuit._last_qubits = q
    chsh_circuit._last_cbits = c
    return prog
