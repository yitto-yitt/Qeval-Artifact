# EVAL_META: task_id=9, framework=qpanda, class=3
from pyqpanda3.core import *


def create_efficientSU2():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(3)
    c = machine.cAlloc_many(3)

    prog = QProg()

    # EfficientSU2 with reps=1, default su2_gates=['ry', 'rz'], entanglement='reverse_linear'
    # Layer 1: single-qubit rotations
    prog << RY(q[0], 0.0) << RZ(q[0], 0.0)
    prog << RY(q[1], 0.0) << RZ(q[1], 0.0)
    prog << RY(q[2], 0.0) << RZ(q[2], 0.0)

    # Barrier (insert_barriers=True)
    prog << BARRIER(q)

    # Entanglement layer: reverse_linear for 3 qubits -> CX(2,1), CX(1,0)
    prog << CNOT(q[2], q[1])
    prog << CNOT(q[1], q[0])

    # Barrier
    prog << BARRIER(q)

    # Layer 2: single-qubit rotations
    prog << RY(q[0], 0.0) << RZ(q[0], 0.0)
    prog << RY(q[1], 0.0) << RZ(q[1], 0.0)
    prog << RY(q[2], 0.0) << RZ(q[2], 0.0)

    return prog
