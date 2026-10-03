# EVAL_META: task_id=145, framework=qiskit, class=3
from qiskit import QuantumCircuit
import numpy as np

def qft_inverse(n):
    qc = QuantumCircuit(n)
    # Swaps at the beginning
    for i in range(n // 2):
        qc.swap(i, n - i - 1)
    # Reverse the QFT steps
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, i, -1):
            qc.cp(-np.pi / (2 ** (j - i)), i, j)
        qc.h(i)
    return qc
