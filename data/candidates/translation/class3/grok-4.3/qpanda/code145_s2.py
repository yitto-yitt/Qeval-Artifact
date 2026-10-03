# EVAL_META: task_id=145, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit, H, CP, SWAP
import math

def qft_inverse(n):
    qc = QuantumCircuit(n)
    for i in range(n):
        qc.append(H(i))
        for j in range(i + 1, n):
            qc.append(CP(j, i, -2 * math.pi / (2 ** (j - i))))
    for qubit in range(n // 2):
        qc.append(SWAP(qubit, n - qubit - 1))
    return qc
