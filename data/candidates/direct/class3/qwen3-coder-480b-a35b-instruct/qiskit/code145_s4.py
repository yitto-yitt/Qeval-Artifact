# EVAL_META: task_id=145, framework=qiskit, class=3

from qiskit import QuantumCircuit
import math

def qft_inverse(n):
    qc = QuantumCircuit(n)
    
    # Apply inverse QFT operations in reverse order
    for j in range(n):
        # Apply Hadamard gate to qubit n-j-1
        qc.h(n-j-1)
        
        # Apply controlled phase gates in reverse order
        for k in range(j):
            # Apply controlled rotation -pi/2^(j-k) between qubits (n-j-1) and (n-k-1)
            angle = -math.pi / (2**(j-k))
            qc.cp(angle, n-k-1, n-j-1)
    
    # Reverse the order of qubits to match standard QFT definition
    for i in range(n//2):
        qc.swap(i, n-i-1)
    
    return qc
