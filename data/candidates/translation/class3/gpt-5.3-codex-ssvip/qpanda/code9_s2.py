# EVAL_META: task_id=9, framework=qpanda, class=3
from pyqpanda3.core import *

def create_efficientSU2():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(3)
    c = machine.cAlloc_many(3)

    prog = QProg()
    pi = 3.141592653589793

    # Initial single-qubit SU2 layer (ry, rz)
    prog << RY(q[0], 0.1 * pi) << RZ(q[0], 0.2 * pi)
    prog << RY(q[1], 0.3 * pi) << RZ(q[1], 0.4 * pi)
    prog << RY(q[2], 0.5 * pi) << RZ(q[2], 0.6 * pi)

    # Barrier equivalent (no-op in pyQPanda3 core API)
    # Entanglement layer (linear)
    prog << CNOT(q[0], q[1]) << CNOT(q[1], q[2])

    # Barrier equivalent (no-op)
    # Final single-qubit SU2 layer (ry, rz)
    prog << RY(q[0], 0.7 * pi) << RZ(q[0], 0.8 * pi)
    prog << RY(q[1], 0.9 * pi) << RZ(q[1], 1.0 * pi)
    prog << RY(q[2], 1.1 * pi) << RZ(q[2], 1.2 * pi)

    return prog
