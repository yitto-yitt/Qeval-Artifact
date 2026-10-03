# EVAL_META: task_id=126, framework=pennylane, class=3
import pennylane as qml
import numpy as np


def calculate_phase_difference_fidelity():
    # Create the first operator (Hadamard gate)
    op_a_matrix = qml.Hadamard.compute_matrix()
    
    # Create the second operator (Hadamard gate with global phase)
    op_b_matrix = np.exp(1j * 0.5) * op_a_matrix
    
    # Calculate process fidelity
    # In PennyLane, we can compute the fidelity between unitary operations
    # Process fidelity for unitaries U1 and U2 is |Tr(U1^dagger U2)|^2 / d^2 where d is dimension
    d = 2  # Dimension of single qubit system
    overlap = np.abs(np.trace(np.conj(op_a_matrix.T) @ op_b_matrix))**2 / (d**2)
    
    return overlap
