# EVAL_META: task_id=139, framework=qiskit, class=2

import numpy as np
from qiskit.quantum_info import DensityMatrix, Statevector
from scipy.linalg import svd


def schmidt_test(data, qargs_B):
    """
    Compute the Schmidt decomposition for a density matrix with respect to a bipartition.
    
    Args:
        data: Density matrix as a 2D array or DensityMatrix object
        qargs_B: List of qubit indices for subsystem B (the rest form subsystem A)
        
    Returns:
        List of tuples (coefficient, state_A, state_B) representing Schmidt terms
    """
    # Convert input to DensityMatrix if needed
    if not isinstance(data, DensityMatrix):
        rho = DensityMatrix(data)
    else:
        rho = data.copy()
    
    # Get total number of qubits
    n_qubits = rho.num_qubits
    
    # Determine qubit indices for subsystem A
    qargs_A = [i for i in range(n_qubits) if i not in qargs_B]
    
    # Get dimensions of subsystems
    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    
    # Partial trace to get reduced density matrices
    rho_A = rho.ptrace(qargs_B)
    rho_B = rho.ptrace(qargs_A)
    
    # Get matrix representation
    rho_matrix = rho.data
    rho_A_matrix = rho_A.data
    rho_B_matrix = rho_B.data
    
    # Reshape the full density matrix according to the bipartition
    # For density matrix elements |i_A i_B><j_A j_B|, reshape to (dim_A, dim_B, dim_A, dim_B)
    reshaped = rho_matrix.reshape(dim_A, dim_B, dim_A, dim_B)
    
    # Rearrange indices to group A and B indices together: (dim_A, dim_A, dim_B, dim_B)
    reshaped = np.transpose(reshaped, (0, 2, 1, 3))
    
    # Reshape to (dim_A*dim_A, dim_B*dim_B) for SVD
    matrix_to_svd = reshaped.reshape(dim_A * dim_A, dim_B * dim_B)
    
    # Perform SVD
    U, s, Vh = svd(matrix_to_svd)
    
    # The singular values are the Schmidt coefficients squared
    # Since we're working with density matrices, take square root to get actual Schmidt coefficients
    schmidt_coeffs = np.sqrt(s)
    
    # Remove near-zero coefficients
    tol = 1e-10
    nonzero_indices = np.where(schmidt_coeffs > tol)[0]
    
    result = []
    
    for idx in nonzero_indices:
        coeff = schmidt_coeffs[idx]
        
        # Extract states from U and Vh
        u_vec = U[:, idx].reshape(dim_A, dim_A)
        vh_vec = Vh[idx, :].reshape(dim_B, dim_B)
        
        # Convert to state vectors by taking eigenvectors of the reduced density matrices
        # For pure states, the Schmidt decomposition comes from the SVD of the state vector
        # But for mixed states, we need to be more careful
        
        # Let's compute the Schmidt decomposition properly by using the purification
        # We'll use the fact that the Schmidt coefficients are the square roots of 
        # the eigenvalues of the reduced density matrices
        
        # Eigenvalue decomposition of reduced density matrices
        evals_A, evecs_A = np.linalg.eigh(rho_A_matrix)
        evals_B, evecs_B = np.linalg.eigh(rho_B_matrix)
        
        # Take positive square roots
        sqrt_evals_A = np.sqrt(np.maximum(evals_A, 0))
        sqrt_evals_B = np.sqrt(np.maximum(evals_B, 0))
        
        # The Schmidt coefficients should be the same from both perspectives
        # Sort them in descending order
        sorted_indices_A = np.argsort(sqrt_evals_A)[::-1]
        sorted_indices_B = np.argsort(sqrt_evals_B)[::-1]
        
        sqrt_evals_A = sqrt_evals_A[sorted_indices_A]
        sqrt_evals_B = sqrt_evals_B[sorted_indices_B]
        evecs_A = evecs_A[:, sorted_indices_A]
        evecs_B = evecs_B[:, sorted_indices_B]
        
        # Only keep significant coefficients
        valid_indices_A = sqrt_evals_A > tol
        valid_indices_B = sqrt_evals_B > tol
        
        if np.sum(valid_indices_A) > idx and np.sum(valid_indices_B) > idx:
            state_A = evecs_A[:, idx]
            state_B = evecs_B[:, idx]
            
            # Normalize states
            norm_A = np.linalg.norm(state_A)
            norm_B = np.linalg.norm(state_B)
            
            if norm_A > tol and norm_B > tol:
                state_A = state_A / norm_A
                state_B = state_B / norm_B
                result.append((coeff, state_A, state_B))
    
    return result
