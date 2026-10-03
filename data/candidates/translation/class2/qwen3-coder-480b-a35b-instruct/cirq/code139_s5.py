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
    
    # Calculate dimensions of partitions
    dim_A = 1 << (n_qubits - len(qargs_B))
    dim_B = 1 << len(qargs_B)
    
    # Reshape the density matrix into a 4-partite tensor: (A, B, A*, B*)
    reshaped_rho = rho.reshape(dim_A, dim_B, dim_A, dim_B)
    
    # Perform SVD on the reshaped matrix treated as a matrix from A*A* to B*B*
    # Transpose to get the right shape for SVD: (A*A*, B*B*)
    M = reshaped_rho.transpose(0, 2, 1, 3).reshape(dim_A * dim_A, dim_B * dim_B)
    
    # Compute the SVD
    U, s, Vh = np.linalg.svd(M, full_matrices=False)
    
    # The singular values are the Schmidt coefficients
    schmidt_coeffs = np.sqrt(s)  # Square root because we're working with density matrix
    
    # Normalize the singular values so they sum to 1 (if dealing with pure state)
    # Actually, for a pure state's reduced density matrix, the sum of squares of schmidt coeffs should be 1
    # So we just need to make sure our calculation is correct
    
    # Filter out negligible coefficients
    threshold = 1e-8
    valid_indices = schmidt_coeffs > threshold
    schmidt_coeffs = schmidt_coeffs[valid_indices]
    
    # Extract corresponding states for each partition
    result = []
    for i in range(len(schmidt_coeffs)):
        # For each Schmidt coefficient, we need to extract the corresponding states
        # This requires more complex tensor operations to get the actual state vectors
        # We'll use the fact that the SVD gives us the decomposition
        
        # Get the corresponding left and right singular vectors
        u_vec = U[:, valid_indices][i]  # State vector for partition A
        v_vec = Vh[valid_indices][i, :]  # State vector for partition B
        
        # Reshape these vectors back to proper quantum state form
        state_A = u_vec.reshape(dim_A, dim_A)
        state_B = v_vec.reshape(dim_B, dim_B)
        
        # For a pure state decomposition, we take one side of each matrix
        # Take the diagonal or appropriate vector representation
        # Actually, let's compute this properly by using the eigenvalue decomposition of reduced density matrices
        
        # Recompute using the proper method: partial trace and eigendecomposition
        # Trace out system B to get reduced density matrix of A
        reduced_A = np.trace(reshaped_rho, axis1=1, axis2=3)  # Partial trace over B
        evals_A, evecs_A = np.linalg.eigh(reduced_A)
        
        # Trace out system A to get reduced density matrix of B  
        reduced_B = np.trace(reshaped_rho, axis1=0, axis2=2)  # Partial trace over A
        evals_B, evecs_B = np.linalg.eigh(reduced_B)
        
        # The eigenvalues should be the same (up to numerical precision), these are the squared schmidt coefficients
        # Take the positive square roots
        schmidt_coeffs = np.sqrt(np.maximum(evals_A, 0))
        
        # Filter out negligible coefficients
        valid_indices = schmidt_coeffs > threshold
        schmidt_coeffs = schmidt_coeffs[valid_indices]
        evecs_A = evecs_A[:, valid_indices]
        evecs_B = evecs_B[:, valid_indices]
        
        # Create the result list
        result = []
        for i in range(len(schmidt_coeffs)):
            coeff = schmidt_coeffs[i]
            state_A = evecs_A[:, i]  # State vector for partition A
            state_B = evecs_B[:, i]  # State vector for partition B
            result.append((coeff, state_A, state_B))
            
        return result
    
    # If no valid coefficients found, return empty list
    return []
