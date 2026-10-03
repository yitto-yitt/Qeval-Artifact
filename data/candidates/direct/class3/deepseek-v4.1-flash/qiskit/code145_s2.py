# EVAL_META: task_id=145, framework=qiskit, class=3
import numpy as np
from qiskit import QuantumCircuit


def qft_inverse(n):
    qc = QuantumCircuit(n)
    for j in reversed(range(n)):
        for k in reversed(range(j + 1, n)):
            qc.cp(-np.pi / (2 ** (k - j)), k, j)
        qc.h(j)
    for qubit in range(n // 2):
        qc.swap(qubit, n - qubit - 1)
    return qc
