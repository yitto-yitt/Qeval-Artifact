# EVAL_META: task_id=145, framework=qiskit, class=3
from qiskit import QuantumCircuit
import numpy as np

def qft_inverse(n):
    qc = QuantumCircuit(n)
    # Swaps
    for i in range(n // 2):
        qc.swap(i, n - i - 1)
    # Reverse QFT
    for j in reversed(range(n)):
        for k in reversed(range(j + 1, n)):
            qc.cp(-np.pi / (2 ** (k - j)), k, j)
        qc.h(j)
    return qc
