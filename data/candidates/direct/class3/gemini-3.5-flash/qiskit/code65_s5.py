# EVAL_META: task_id=65, framework=qiskit, class=3
import numpy as np
from qiskit import QuantumCircuit

def QFT(n):
    """Generates a Quantum Fourier Transform circuit for n qubits."""
    qc = QuantumCircuit(n)
    if n == 0:
        return qc
    for i in range(n - 1, -1, -1):
        qc.h(i)
        for j in range(i - 1, -1, -1):
            angle = np.pi / (2 ** (i - j))
            qc.cp(angle, j, i)
    # Swap qubits to match standard QFT representation
    for i in range(n // 2):
        qc.swap(i, n - i - 1)
    return qc
