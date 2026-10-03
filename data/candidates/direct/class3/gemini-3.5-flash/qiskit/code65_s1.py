# EVAL_META: task_id=65, framework=qiskit, class=3
from qiskit import QuantumCircuit
import numpy as np

def QFT(n: int) -> QuantumCircuit:
    qc = QuantumCircuit(n)
    if n == 0:
        return qc
    for i in range(n - 1, -1, -1):
        qc.h(i)
        for j in range(i - 1, -1, -1):
            angle = np.pi / (2 ** (i - j))
            qc.cp(angle, j, i)
    
    for i in range(n // 2):
        qc.swap(i, n - 1 - i)
        
    return qc
