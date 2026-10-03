# EVAL_META: task_id=139, framework=cirq, class=2
import cirq
import numpy as np
from typing import List, Tuple

def schmidt_test(data, qargs_B):
    # Convert input to numpy array if it's not already
    rho = np.asarray(data)
    
    # Get dimensions
    dim_total = rho.shape[0]
    n_qubits = int(np.log2(dim_total))
    
    # Calculate dimensions of subsystems
    dim_A = 2 ** (n_qubits - len(qargs_B))
    dim_B = 2 ** len(qargs_B)
    
    # Reshape the density matrix to a 4D tensor representing the bipartite system
    # Original shape: (dim_total, dim_total) -> (dim_A, dim_B, dim_A, dim_B)
    reshaped_rho = rho.reshape(dim_A, dim_B, dim_A, dim_B)
    
    # Perform SVD on the reshaped matrix treated as a matrix of size (dim_A*dim_B, dim_A*dim_B)
    # We need to reshape to get the operator in the form where we can extract Schmidt coefficients
    M = reshaped_rho.transpose(0, 2, 1, 3).reshape(dim_A * dim_A, dim_B * dim_B)
    
    # For pure states, we would work with the state vector directly
    # But since we have a density matrix, we need to find its eigenvalues and eigenvectors
    eigenvals, eigenvecs = np.linalg.eigh(rho)
    
    # Only consider non-zero eigenvalues
    nonzero_idx = np.where(eigenvals > 1e-12)[0]
    eigenvals = eigenvals[nonzero_idx]
    eigenvecs = eigenvecs[:, nonzero_idx]
    
    # For each eigenvalue/vector pair, decompose the corresponding pure state
    results = []
    
    for i in range(len(eigenvals)):
        if eigenvals[i] <= 1e-12:
            continue
            
        # Get the pure state corresponding to this eigenvalue
        psi = eigenvecs[:, i]
        
        # Reshape the state vector to (dim_A, dim_B)
        psi_reshaped = psi.reshape(dim_A, dim_B)
        
        # Perform SVD to get Schmidt decomposition
        U, schmidt_coeffs, Vh = np.linalg.svd(psi_reshaped)
        
        # Add each Schmidt term to the result
        for j in range(len(schmidt_coeffs)):
            if schmidt_coeffs[j] > 1e-12:
                # Create subsystem states
                state_A = U[:, j]
                state_B = Vh[j, :].conj()  # Conjugate for proper definition
                
                results.append((schmidt_coeffs[j], state_A, state_B))
    
    return results
