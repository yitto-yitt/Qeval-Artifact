# EVAL_META: task_id=145, framework=qiskit, class=3

import numpy as np
from qiskit import QuantumCircuit

def qft_inverse(n):
    qc = QuantumCircuit(n)
    # Swap qubits to reverse order (required for inverse QFT)
    for i in range(n // 2):
        qc.swap(i, n - 1 - i)
    # Apply inverse QFT gates
    for i in reversed(range(n)):
        qc.h(i)
        for j in range(n - 1, i, -1):
            angle = -np.pi / (2 ** (j - i))
            qc.cp(angle, j, i)
    return qc
