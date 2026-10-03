# EVAL_META: task_id=145, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np
machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(20)
def qft_inverse(n):
    q = qubits[:n]
    circ = QCircuit()
    for i in range(n):
        for j in range(i):
            circ << CR(q[j], q[i], -np.pi / (2 ** (i - j)))
        circ << H(q[i])
    for i in range(n // 2):
        circ << SWAP(q[i], q[n - 1 - i])
    return circ
machine.finalize()
