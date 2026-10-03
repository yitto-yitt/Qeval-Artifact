# EVAL_META: task_id=145, framework=qiskit, class=3
from math import pi
from qiskit.circuit import QuantumCircuit

def qft_inverse(n):
    qc = QuantumCircuit(n)
    for j in range(n // 2):
        qc.swap(j, n - j - 1)
    for j in reversed(range(n)):
        for k in reversed(range(j + 1, n)):
            qc.cp(-pi / (2 ** (k - j)), k, j)
        qc.h(j)
    return qc
