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
        # Convert statevector to density matrix for uniform processing
        rho = DensityMatrix(data)
        psi = data
    elif isinstance(data, DensityMatrix):
        rho = data
        # For now, we assume the input is a pure state density matrix
        # Extract the pure state using eigenvalue decomposition
        evals, evecs = np.linalg.eigh(rho.data)
        # Find the eigenvector with the largest eigenvalue (should be 1 for pure state)
        max_idx = np.argmax(evals)
        psi = Statevector(evecs[:, max_idx])
    else:
        raise ValueError("Input must be a Statevector or DensityMatrix")
    
    # Get the full state vector
    state_vector = psi.data
    
    n_qubits = int(np.log2(len(state_vector)))
    
    # Define subsystem A as complement of B
    all_qubits = set(range(n_qubits))
    qargs_A = sorted(list(all_qubits - set(qargs_B)))
    
    # Reshape the state vector into a matrix form for Schmidt decomposition
    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    
    # Create a mapping from computational basis states to the tensor product structure
    reshaped_state = state_vector.reshape((dim_A, dim_B))
    
    # Perform SVD on the reshaped state
    U, s, Vh = np.linalg.svd(reshaped_state, full_matrices=False)
    
    # The singular values are the Schmidt coefficients
    schmidt_coeffs = s
    
    # Filter out negligible coefficients
    threshold = 1e-8
    significant_indices = np.where(schmidt_coeffs > threshold)[0]
    
    result = []
    for idx in significant_indices:
        coeff = schmidt_coeffs[idx]
        state_A = U[:, idx]  # State vector for subsystem A
        state_B = Vh[idx, :]  # State vector for subsystem B
        
        result.append((coeff, state_A, state_B))
    
    return result
