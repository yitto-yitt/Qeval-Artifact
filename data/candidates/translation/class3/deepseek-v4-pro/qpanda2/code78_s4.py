# EVAL_META: task_id=78, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np

machine = CPUQVM()
machine.init_qvm()
_qft_qubits = []

def qft_no_swaps(num_qubits):
    q = machine.qAlloc_many(num_qubits)
    _qft_qubits.append(q)
    prog = QProg()
    for j in range(num_qubits - 1, -1, -1):
        for k in range(num_qubits - 1, j, -1):
            prog << CPHASE(q[k], q[j], -np.pi / (2 ** (k - j)))
        prog << H(q[j])
    return prog

machine.finalize()
