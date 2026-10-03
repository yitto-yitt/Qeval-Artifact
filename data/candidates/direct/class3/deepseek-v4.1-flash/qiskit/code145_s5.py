# EVAL_META: task_id=145, framework=qiskit, class=3
import numpy as np
from qiskit import QuantumCircuit


def qft_inverse(n):
    qc = QuantumCircuit(n, name="qft_inverse")
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, i, -1):
            qc.cp(-np.pi / (2 ** (j - i)), j, i)
        qc.h(i)
    return qc
