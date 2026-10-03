# EVAL_META: task_id=139, framework=cirq, class=2
import cirq
import numpy as np
from typing import List, Tuple, Union

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
    # We need to rearrange indices to get the proper form for SVD
    # Reshape to (dim_A * dim_B, dim_A * dim_B)
    matrix_for_svd = reshaped_rho.transpose(0, 1, 2, 3).reshape(dim_A * dim_B, dim_A * dim_B)
    
    # Perform SVD
    U, s, Vh = np.linalg.svd(matrix_for_svd)
    
    # Extract Schmidt coefficients (square roots of eigenvalues of reduced density matrices)
    schmidt_coeffs = np.sqrt(s)
    
    # Filter out negligible coefficients
    tolerance = 1e-8
    valid_indices = schmidt_coeffs > tolerance
    
    schmidt_coeffs = schmidt_coeffs[valid_indices]
    U = U[:, valid_indices]
    Vh = Vh[valid_indices, :]
    
    result = []
    for i in range(len(schmidt_coeffs)):
        coeff = schmidt_coeffs[i]
        
        # Extract the corresponding vectors for subsystems A and B
        # U[:, i] and Vh[i, :] need to be reshaped back to (dim_A, dim_B) form
        u_vec = U[:, i].reshape(dim_A, dim_B)
        v_vec = Vh[i, :].reshape(dim_A, dim_B)
        
        # For a pure state decomposition, we extract the corresponding vectors
        # In the case of mixed states, this becomes more complex
        # Here we assume we're working with a pure state or want the decomposition of the purification
        
        # For each valid Schmidt coefficient, create the corresponding subsystem states
        # The state vector for A would be the corresponding column of U reshaped appropriately
        # The state vector for B would be the corresponding row of Vh reshaped appropriately
        
        # Extract subsystem A state (normalize if needed)
        subsystem_A_state = u_vec[:, 0]  # Simplified approach
        if np.linalg.norm(subsystem_A_state) > 1e-10:
            subsystem_A_state = subsystem_A_state / np.linalg.norm(subsystem_A_state)
        
        # Extract subsystem B state (normalize if needed)  
        subsystem_B_state = v_vec[0, :]  # Simplified approach
        if np.linalg.norm(subsystem_B_state) > 1e-10:
            subsystem_B_state = subsystem_B_state / np.linalg.norm(subsystem_B_state)
        
        result.append((coeff, subsystem_A_state, subsystem_B_state))
    
    return result
