# EVAL_META: task_id=126, framework=qiskit, class=3
import numpy as np
from qiskit.quantum_info import Operator, process_fidelity

def calculate_phase_difference_fidelity():
    """
    Create two quantum operators using Hadamard gate that differ only by a global phase.
    Calculate the process fidelity between these two operators and return the value.
    """
    # Hadamard matrix
    h_matrix = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
    
    # Operator 1: Standard Hadamard
    op1 = Operator(h_matrix)
    
    # Operator 2: Hadamard with a global phase of e^{i * pi / 4}
    op2 = Operator(np.exp(1j * np.pi / 4) * h_matrix)
    
    # Calculate process fidelity
    fidelity = process_fidelity(op1, op2)
    
    return fidelity
