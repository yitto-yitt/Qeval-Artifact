# EVAL_META: task_id=65, framework=qiskit, class=3
from qiskit import QuantumCircuit
import numpy as np

def QFT(n):
    qc = QuantumCircuit(n, name='QFT')
    for j in range(n - 1, -1, -1):
        qc.h(j)
        for k in range(j - 1, -1, -1):
            qc.cp(np.pi / (2 ** (j - k)), k, j)
    for j in range(n // 2):
        qc.swap(j, n - 1 - j)
    return qc
