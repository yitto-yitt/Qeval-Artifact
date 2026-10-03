# EVAL_META: task_id=78, framework=qiskit, class=3
from qiskit import QuantumCircuit
import math

def qft_no_swaps(num_qubits):
    qc = QuantumCircuit(num_qubits)
    
    # Apply inverse QFT operations without swaps
    for i in range(num_qubits - 1, -1, -1):
        # Apply Hadamard gate to current qubit
        qc.h(i)
        
        # Apply controlled phase rotations
        for j in range(i - 1, -1, -1):
            angle = -2 * math.pi / (2 ** (i - j + 1))
            qc.cp(angle, i, j)
            
    return qc
