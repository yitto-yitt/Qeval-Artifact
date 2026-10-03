# EVAL_META: task_id=65, framework=qiskit, class=3
import math
from qiskit import QuantumCircuit

def QFT(n):
    qc = QuantumCircuit(n)
    for j in range(n):
        qc.h(j)
        for k in range(j + 1, n):
            qc.cp(math.pi / (2 ** (k - j)), k, j)
    for j in range(n // 2):
        qc.swap(j, n - j - 1)
    return qc
