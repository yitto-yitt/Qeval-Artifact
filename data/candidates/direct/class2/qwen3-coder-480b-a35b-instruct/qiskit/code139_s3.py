# EVAL_META: task_id=139, framework=qiskit, class=2

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info import DensityMatrix, Statevector


def schmidt_test(data, qargs_B):
    """
    Compute the Schmidt decomposition of a pure state or density matrix.
    
    Args:
        data: A Statevector or DensityMatrix object representing the quantum state
        qargs_B: List of qubit indices corresponding to subsystem B (complement is A)
        
    Returns:
        List of tuples (coefficient, state_A, state_B) representing the Schmidt decomposition
    """
    if isinstance(data, Statevector):
        # Convert statevector to density matrix
        dm = DensityMatrix(data)
        psi = data.data
        n_qubits = data.num_qubits
    elif isinstance(data, DensityMatrix):
        # For density matrices, we assume it's a pure state and extract its purification
        dm = data
        n_qubits = data.num_qubits
        # Get eigenvalues and eigenvectors
        evals, evecs = np.linalg.eigh(dm.data)
        # Find the non-zero eigenvalue (for pure states there should be one close to 1)
        max_idx = np.argmax(evals)
        psi = evecs[:, max_idx]
    else:
        raise ValueError("Data must be a Statevector or DensityMatrix")

    # Total number of qubits
    n_total = n_qubits
    
    # Define subsystem A as complement of B
    all_qubits = set(range(n_total))
    qargs_A = sorted(list(all_qubits - set(qargs_B)))
    
    # Number of qubits in each subsystem
    n_A = len(qargs_A)
    n_B = len(qargs_B)
    
    # Dimension of each subsystem
    dim_A = 2 ** n_A
    dim_B = 2 ** n_B
    
    # Reshape the state vector into a matrix of shape (dim_A, dim_B)
    psi_matrix = psi.reshape((dim_A, dim_B))
    
    # Perform SVD on the reshaped matrix
    U, s, Vh = np.linalg.svd(psi_matrix, full_matrices=False)
    
    # Extract the Schmidt coefficients (s) and normalize
    schmidt_coeffs = s
    
    # Filter out negligible coefficients (to handle numerical errors)
    threshold = 1e-8
    valid_indices = schmidt_coeffs > threshold
    
    result = []
    for i in range(len(schmidt_coeffs)):
        if valid_indices[i]:
            coeff = schmidt_coeffs[i]
            state_A = U[:, i]  # State vector for subsystem A
            state_B = Vh[i, :]  # State vector for subsystem B (V is already conjugate transposed)
            
            result.append((coeff, state_A, state_B))
    
    return result
