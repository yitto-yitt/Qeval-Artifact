# EVAL_META: task_id=145, framework=qiskit, class=3
import numpy as np
from qiskit import QuantumCircuit

def qft_inverse(n):
    qc = QuantumCircuit(n)
    for qubit in range(n // 2):
        qc.swap(qubit, n - qubit - 1)
    for j in range(n):
        for m in range(j):
            qc.cp(-np.pi / float(2 ** (j - m)), m, j)
        qc.h(j)
    return qc
