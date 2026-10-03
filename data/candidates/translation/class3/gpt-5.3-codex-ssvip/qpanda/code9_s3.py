# EVAL_META: task_id=9, framework=qpanda, class=3
from pyqpanda3.core import *

def create_efficientSU2():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(3)
    c = machine.cAlloc_many(3)

    prog = QProg()

    # EfficientSU2 with reps=1, default su2_gates=['ry','rz'], entanglement='reverse_linear'
    # Layer 0
    prog << RY(q[0], 0.0) << RZ(q[0], 0.0)
    prog << RY(q[1], 0.0) << RZ(q[1], 0.0)
    prog << RY(q[2], 0.0) << RZ(q[2], 0.0)

    # Barrier (insert_barriers=True) - represented as no-op separator in pyQPanda
    # Entanglement layer (reverse_linear for 3 qubits): CX(2,1), CX(1,0)
    prog << CNOT(q[2], q[1])
    prog << CNOT(q[1], q[0])

    # Barrier
    # Final SU2 layer
    prog << RY(q[0], 0.0) << RZ(q[0], 0.0)
    prog << RY(q[1], 0.0) << RZ(q[1], 0.0)
    prog << RY(q[2], 0.0) << RZ(q[2], 0.0)

    # Execute through framework
    machine.directly_run(prog)

    return prog
