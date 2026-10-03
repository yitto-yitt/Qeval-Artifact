# EVAL_META: task_id=65, framework=qiskit, class=3
from qiskit import QuantumCircuit
from math import pi

def QFT(n):
    qc = QuantumCircuit(n)
    for j in range(n):
        qc.h(j)
        for k in range(j + 1, n):
            qc.cp(pi / (2 ** (k - j)), k, j)
    for i in range(n // 2):
        qc.swap(i, n - i - 1)
    return qc
