# EVAL_META: task_id=78, framework=qiskit, class=3
from qiskit import QuantumCircuit
import math

def qft_no_swaps(num_qubits):
    """Return an inverse quantum Fourier transform circuit without the swap gates."""
    qc = QuantumCircuit(num_qubits)
    
    # Apply inverse QFT operations in reverse order compared to regular QFT
    for j in range(num_qubits):
        # Apply Hadamard gate
        qc.h(j)
        
        # Apply controlled phase shift gates in reverse order
        for k in range(j + 1, num_qubits):
            angle = -2 * math.pi / (2 ** (k - j + 1))
            qc.cp(angle, k, j)
            
    return qc
