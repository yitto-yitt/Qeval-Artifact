# EVAL_META: task_id=145, framework=qiskit, class=3
import math

from qiskit import QuantumCircuit


def qft_inverse(n):
    qc = QuantumCircuit(n)
    for i in range(n // 2):
        qc.swap(i, n - 1 - i)
    for i in range(n):
        for j in range(i):
            qc.cp(-math.pi / (2 ** (i - j)), j, i)
        qc.h(i)
    return qc
