# EVAL_META: task_id=126, framework=pennylane, class=3
import pennylane as qml
import numpy as np


def calculate_phase_difference_fidelity():
    # Create the Hadamard operator
    hadamard_matrix = qml.matrix(qml.Hadamard)(wires=[0])
    
    # Create the second operator with a global phase difference
    op_a = hadamard_matrix
    op_b = np.exp(1j * 0.5) * hadamard_matrix
    
    # Calculate process fidelity using the formula for unitary operators
    # Process fidelity between two unitary operators U1 and U2 is |Tr(U1^\dagger U2)|^2 / d^2
    # where d is the dimension of the operator
    d = op_a.shape[0]
    fidelity = np.abs(np.trace(np.conj(op_a.T) @ op_b))**2 / (d**2)
    
    return fidelity
