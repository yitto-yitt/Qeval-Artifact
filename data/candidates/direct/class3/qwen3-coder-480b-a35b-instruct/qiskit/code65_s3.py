# EVAL_META: task_id=65, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import U1Gate
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
    
    # Apply Hadamard and controlled phase rotations for each qubit
    for i in range(n):
        # Apply Hadamard gate to current qubit
        qc.h(i)
        
        # Apply controlled phase rotations to remaining qubits
        for j in range(i + 1, n):
            # Calculate angle for rotation
            angle = math.pi / (2 ** (j - i))
            # Apply controlled U1 gate
            qc.cp(angle, j, i)
    
    # Reverse the order of qubits to get standard QFT output
    for i in range(n // 2):
        qc.swap(i, n - 1 - i)
    
    return qc
