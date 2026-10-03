# EVAL_META: task_id=145, framework=qiskit, class=3
from qiskit import QuantumCircuit
import numpy as np

def qft_inverse(n):
    qc = QuantumCircuit(n)
    for qubit in range(n // 2):
        qc.swap(qubit, n - qubit - 1)
    for j in range(n):
        qc.h(j)
        for k in range(j):
            qc.cp(-np.pi / float(2 ** (j - k)), k, j)
    return qc
