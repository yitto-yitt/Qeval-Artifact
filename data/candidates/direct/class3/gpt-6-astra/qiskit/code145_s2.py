# EVAL_META: task_id=145, framework=qiskit, class=3
from math import pi
from qiskit import QuantumCircuit


def qft_inverse(n):
    qc = QuantumCircuit(n, name="QFT†")
    for j in range(n // 2):
        qc.swap(j, n - j - 1)
    for j in range(n):
        for m in range(j):
            qc.cp(-pi / (2 ** (j - m)), m, j)
        qc.h(j)
    return qc
