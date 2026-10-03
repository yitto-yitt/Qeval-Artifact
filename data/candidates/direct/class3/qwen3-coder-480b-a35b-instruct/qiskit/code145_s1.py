# EVAL_META: task_id=145, framework=qiskit, class=3
from qiskit import QuantumCircuit
import numpy as np

def qft_inverse(n):
    qc = QuantumCircuit(n)
    
    # Apply the inverse QFT by reversing the QFT operations
    # Start from the last qubit and work backwards
    for i in range(n-1, -1, -1):
        # Apply Hadamard gate
        qc.h(i)
        
        # Apply controlled phase rotations
        for j in range(i-1, -1, -1):
            angle = -np.pi / (2 ** (i - j))
            qc.cp(angle, j, i)
    
    return qc
