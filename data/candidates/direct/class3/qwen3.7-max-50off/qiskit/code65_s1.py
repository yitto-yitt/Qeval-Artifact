# EVAL_META: task_id=65, framework=qiskit, class=3
from qiskit import QuantumCircuit
import numpy as np


def QFT(n):
    qc = QuantumCircuit(n)
    for i in range(n):
        qc.h(i)
        for j in range(i + 1, n):
            k = j - i + 1
            angle = 2 * np.pi / (2 ** k)
            qc.cp(angle, j, i)
    for i in range(n // 2):
        qc.swap(i, n - i - 1)
    return qc
