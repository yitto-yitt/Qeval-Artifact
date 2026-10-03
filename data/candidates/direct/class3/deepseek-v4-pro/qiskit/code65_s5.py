# EVAL_META: task_id=65, framework=qiskit, class=3
from qiskit import QuantumCircuit
from math import pi

def QFT(n):
    qc = QuantumCircuit(n)
    for q in range(n):
        qc.h(q)
        for c in range(q + 1, n):
            qc.cp(pi / (2 ** (c - q)), c, q)
    for i in range(n // 2):
        qc.swap(i, n - i - 1)
    return qc
