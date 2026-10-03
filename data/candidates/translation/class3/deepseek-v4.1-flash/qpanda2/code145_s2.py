# EVAL_META: task_id=145, framework=qpanda2, class=3
import numpy as np
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(20)

def qft_inverse(n):
    circuit = QCircuit()
    for i in range(n // 2):
        circuit << SWAP(qubits[i], qubits[n - 1 - i])
    for j in range(n - 1, -1, -1):
        for k in range(n - 1, j, -1):
            angle = -np.pi / (2 ** (k - j))
            circuit << CR(qubits[j], qubits[k], angle)
        circuit << H(qubits[j])
    return circuit

machine.finalize()
