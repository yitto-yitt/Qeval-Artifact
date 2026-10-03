# EVAL_META: task_id=126, framework=pennylane, class=3
import pennylane as qml
import numpy as np


def calculate_phase_difference_fidelity():
    # Create the Hadamard matrix
    hadamard_matrix = 1/np.sqrt(2) * np.array([[1, 1], [1, -1]])
    
    # First operator (Hadamard)
    op_a = hadamard_matrix
    
    # Second operator (Hadamard with global phase)
    op_b = np.exp(1j * 0.5) * hadamard_matrix
    
    # Calculate process fidelity
    # For single-qubit gates, process fidelity can be computed as |Tr(U1^dag U2)|^2 / d^2
    # where d is the dimension (2 for single qubit)
    trace_val = np.trace(np.conj(op_a.T) @ op_b)
    fidelity = np.abs(trace_val)**2 / 4
    
    return fidelity
