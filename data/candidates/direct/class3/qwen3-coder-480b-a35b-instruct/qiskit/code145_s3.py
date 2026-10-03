# EVAL_META: task_id=145, framework=qiskit, class=3
from qiskit import QuantumCircuit
import math

def qft_inverse(n):
    qc = QuantumCircuit(n)
    
    # Apply inverse QFT operations in reverse order
    for j in range(n):
        # Apply Hadamard gate to qubit j
        qc.h(j)
        
        # Apply controlled phase shift gates in reverse order
        for k in range(j + 1, n):
            angle = -math.pi / (2 ** (k - j))
            qc.cp(angle, k, j)
    
    # Reverse the order of qubits to match standard QFT definition
    for i in range(n // 2):
        qc.swap(i, n - 1 - i)
    
    return qc
