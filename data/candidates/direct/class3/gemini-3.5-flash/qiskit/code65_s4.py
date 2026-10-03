# EVAL_META: task_id=65, framework=qiskit, class=3

import numpy as np
from qiskit import QuantumCircuit

def QFT(n: int) -> QuantumCircuit:
    """Generates a Quantum Fourier Transform circuit for n qubits."""
    qc = QuantumCircuit(n)
    for i in range(n - 1, -1, -1):
        qc.h(i)
        for j in range(i - 1, -1, -1):
            qc.cp(np.pi / (2 ** (i - j)), j, i)
            
    # Swap registers to match the standard QFT output order
    for i in range(n // 2):
        qc.swap(i, n - i - 1)
        
    return qc
