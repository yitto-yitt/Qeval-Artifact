# EVAL_META: task_id=126, framework=qiskit, class=3
import numpy as np
from qiskit.quantum_info import Operator, process_fidelity

def calculate_phase_difference_fidelity():
    # Create Hadamard operator
    H_matrix = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
    op1 = Operator(H_matrix)
    
    # Create Hadamard operator with a global phase
    op2 = Operator(np.exp(1j * np.pi / 4) * H_matrix)
    
    # Calculate process fidelity
    fidelity = process_fidelity(op1, op2)
    return fidelity
