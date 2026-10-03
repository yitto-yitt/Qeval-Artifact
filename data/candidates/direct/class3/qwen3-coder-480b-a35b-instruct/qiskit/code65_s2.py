# EVAL_META: task_id=65, framework=qiskit, class=3
from qiskit import QuantumCircuit
import math

def QFT(n):
    """
    Create a Quantum Fourier Transform circuit for n qubits.
    
    Args:
        n (int): Number of qubits
    
    Returns:
        QuantumCircuit: A quantum circuit implementing QFT on n qubits
    """
    qc = QuantumCircuit(n)
    
    # Apply QFT to each qubit in order
    for i in range(n):
        # Apply Hadamard gate to current qubit
        qc.h(i)
        
        # Apply controlled phase shift gates to remaining qubits
        for j in range(i + 1, n):
            # Calculate the angle for the controlled rotation
            angle = 2 * math.pi / (2 ** (j - i + 1))
            # Apply controlled phase rotation
            qc.cp(angle, j, i)
    
    # Reverse the order of qubits to get the correct output
    for i in range(n // 2):
        qc.swap(i, n - 1 - i)
    
    return qc
