# EVAL_META: task_id=12, framework=qpanda2, class=3
import numpy as np
from pyqpanda import *

# Initialize CPUQVM and qAlloc_many at the global scope
machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)


def get_unitary():
    prog = QProg()
    # Map Qiskit's LSB-first to pyQPanda's MSB-first
    # Qiskit q0 -> pyQPanda q1
    # Qiskit q1 -> pyQPanda q0
    prog << H(q[1]) << CNOT(q[1], q[0])

    # Get the unitary matrix
    u = get_unitary(prog)
    return np.array(u).reshape(4, 4)


# Manual Cleanup
machine.finalize()
