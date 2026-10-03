# EVAL_META: task_id=12, framework=qpanda2, class=3
import atexit
import numpy as np
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def get_unitary():
    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1])
    return np.array(get_matrix(prog), dtype=complex)


atexit.register(machine.finalize)
