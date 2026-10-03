# EVAL_META: task_id=78, framework=qiskit, class=3
from qiskit import QuantumCircuit
import math

def qft_no_swaps(num_qubits):
    """Return an inverse quantum Fourier transform circuit without the swap gates."""
    qc = QuantumCircuit(num_qubits)
    
    # Apply inverse QFT operations in reverse order compared to regular QFT
    for i in range(num_qubits - 1, -1, -1):
        # Apply Hadamard gate
        qc.h(i)
        
        # Apply controlled phase rotations in reverse order
        for j in range(i):
            angle = -math.pi / (2 ** (i - j))
            qc.cp(angle, j, i)
            
    return qc
