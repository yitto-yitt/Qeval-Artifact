# EVAL_META: task_id=78, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(16)


def qft_no_swaps(num_qubits):
    prog = QProg()
    for j in range(num_qubits):
        target = num_qubits - 1 - j
        for k in range(j):
            control = num_qubits - 1 - k
            angle = -np.pi / (2 ** (j - k))
            prog << CR(qubits[control], qubits[target], angle)
        prog << H(qubits[target])
    return prog
