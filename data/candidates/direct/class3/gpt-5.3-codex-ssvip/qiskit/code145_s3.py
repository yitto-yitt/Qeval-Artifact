# EVAL_META: task_id=145, framework=qiskit, class=3
from qiskit import QuantumCircuit
from math import pi

def qft_inverse(n):
    qc = QuantumCircuit(n)
    for j in range(n // 2):
        qc.swap(j, n - j - 1)
    for j in range(n):
        for k in range(j):
            qc.cp(-pi / (2 ** (j - k)), j, k)
        qc.h(j)
    return qc
