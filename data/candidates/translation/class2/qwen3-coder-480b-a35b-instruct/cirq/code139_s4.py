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
    reshaped_rho = rho.reshape((dim_A, dim_B, dim_A, dim_B))
    
    # Perform SVD on the reshaped matrix treated as a matrix of size (dim_A*dim_B, dim_A*dim_B)
    # We need to reshape to (dim_A * dim_B, dim_A * dim_B) then do SVD-like decomposition
    M = reshaped_rho.transpose(0, 2, 1, 3).reshape((dim_A * dim_A, dim_B * dim_B))
    
    # To get the Schmidt decomposition, we need to work with the purification of the density matrix
    # First, find eigenvalues and eigenvectors of the density matrix
    eigenvals, eigenvecs = np.linalg.eigh(rho)
    
    # Only keep non-zero eigenvalues (with some tolerance for numerical errors)
    tol = 1e-12
    mask = eigenvals > tol
    eigenvals = eigenvals[mask]
    eigenvecs = eigenvecs[:, mask]
    
    # For each eigenvalue and eigenvector, we can form the Schmidt decomposition
    # by reshaping the eigenvectors appropriately
    
    # Actually, let's approach this differently - we'll use the fact that 
    # any pure state can be written in Schmidt form, and for mixed states,
    # we consider purifications
    
    # For a general density matrix, we compute its spectral decomposition
    # Then for each eigenstate, we perform Schmidt decomposition
    
    # However, the most direct way is to use the singular value decomposition
    # of the reshaped matrix where we vectorize the density matrix
    
    # Let's implement the proper Schmidt decomposition algorithm
    # Reshape the density matrix to treat it as an operator from A to B
    # This involves reshaping to (dim_A, dim_B, dim_A, dim_B) and then 
    # performing appropriate SVD
    
    # For a pure state |psi>, the Schmidt decomposition is |psi> = sum_i s_i |u_i>|v_i>
    # For a mixed state, we work with its purification or spectral decomposition
    
    # The correct approach is to find the spectral decomposition of the density matrix
    # Then for each eigenstate, find its Schmidt decomposition
    
    # For each eigenstate, reshape it to the bipartite form and find SVD
    schmidt_terms = []
    
    for i in range(len(eigenvals)):
        if eigenvals[i] <= tol:
            continue
            
        # Get the eigenstate
        psi = eigenvecs[:, i]
        
        # Reshape to bipartite form (dim_A, dim_B)
        psi_reshaped = psi.reshape((dim_A, dim_B))
        
        # Perform SVD to get Schmidt decomposition
        U, schmidt_coeffs, Vh = np.linalg.svd(psi_reshaped)
        
        # The singular values are the square roots of the eigenvalues of reduced density matrices
        # But since we're working with normalized states, we need to account for the eigenvalue
        
        # For each Schmidt coefficient, create the corresponding term
        sqrt_eigenval = np.sqrt(eigenvals[i])
        for j, coeff in enumerate(schmidt_coeffs):
            if abs(coeff) > tol:  # Only include non-negligible coefficients
                # Scale the coefficient by sqrt of the eigenvalue
                scaled_coeff = sqrt_eigenval * coeff
                subsystem_A = U[:, j]
                subsystem_B = Vh[j, :].conj()  # Take conjugate for proper definition
                
                schmidt_terms.append([scaled_coeff, subsystem_A, subsystem_B])
    
    # Actually, the above approach is getting complex. Let me implement a more direct method
    # based on the standard Schmidt decomposition algorithm for pure states
    # and extend it properly for mixed states.
    
    # For a mixed state represented by density matrix rho, 
    # we can think of it as a purification and then apply Schmidt decomposition
    
    # The correct implementation should be:
    # 1. Find the spectral decomposition of the density matrix
    # 2. For each eigenstate, find its Schmidt decomposition
    # 3. Combine appropriately
    
    # Let's go back to basics and implement the proper algorithm
    # Since this is a mixed state, we need to work with the purification
    
    # For now, let's implement the basic SVD-based approach for the matrix reshaped appropriately
    # Treat the density matrix as a bipartite pure state in the purification space
    
    # More accurately, we need to work with the Cholesky decomposition or similar
    # to represent the density matrix in a form suitable for Schmidt decomposition
    
    # Actually, let's implement the proper algorithm:
    # The Schmidt decomposition of a bipartite state |psi> in H_A ⊗ H_B is:
    # |psi> = sum_i lambda_i |u_i>_A ⊗ |v_i>_B
    # where lambda_i >= 0 and sum_i lambda_i^2 = 1
    
    # For a density matrix, we might be looking for something different
    # Let me implement based on the standard definition
    
    # If data represents a pure state vector
    if len(rho.shape) == 1 or rho.shape[0] == rho.shape[1] and np.allclose(rho @ rho, rho, rtol=1e-5, atol=1e-8):
        # It's likely a pure state or density matrix
        # If it's a pure state vector
        if len(rho.shape) == 1:
            psi = rho
            psi_reshaped = psi.reshape((dim_A, dim_B))
            
            U, schmidt_coeffs, Vh = np.linalg.svd(psi_reshaped)
            
            schmidt_terms = []
            for i, coeff in enumerate(schmidt_coeffs):
                if abs(coeff) > 1e-12:
                    schmidt_terms.append([coeff, U[:, i], Vh[i, :]])
                    
            return schmidt_terms
        else:
            # It's a density matrix - find its purification and decompose
            # Or work with the spectral decomposition
            eigenvals, eigenvecs = np.linalg.eigh(rho)
            # Only positive eigenvalues
            pos_mask = eigenvals > 1e-12
            eigenvals = eigenvals[pos_mask]
            eigenvecs = eigenvecs[:, pos_mask]
            
            # For each eigenstate, find Schmidt decomposition
            all_terms = []
            for idx in range(len(eigenvals)):
                state = eigenvecs[:, idx]
                state_reshaped = state.reshape((dim_A, dim_B))
                
                U, s_coeffs, Vh = np.linalg.svd(state_reshaped)
                
                sqrt_eval = np.sqrt(eigenvals[idx])
                for j, sc in enumerate(s_coeffs):
                    if abs(sc) > 1e-12:
                        all_terms.append([sqrt_eval * sc, U[:, j], Vh[j, :]])
                        
            return all_terms
    else:
        # General case - work with the matrix directly
        # Reshape to treat as a bipartite operator
        reshaped_data = rho.reshape((dim_A, dim_B, dim_A, dim_B))
        
        # This is getting quite complex for mixed states
        # Let's implement a simpler but correct version
        
        # For a pure state |psi>, reshape it to (dim_A, dim_B)
        # Then perform SVD to get Schmidt coefficients and vectors
        eigenvals, eigenvecs = np.linalg.eigh(rho)
        pos_mask = eigenvals > 1e-12
        eigenvals = eigenvals[pos_mask]
        eigenvecs = eigenvecs[:, pos_mask]
        
        result = []
        for i in range(len(eigenvals)):
            state = eigenvecs[:, i]
            state_reshaped = state.reshape((dim_A, dim_B))
            
            U, s, Vh = np.linalg.svd(state_reshaped)
            
            sqrt_lambda = np.sqrt(eigenvals[i])
            for k in range(len(s)):
                if abs(s[k]) > 1e-12:
                    result.append([
                        sqrt_lambda * s[k],
                        U[:, k],
                        Vh[k, :]
                    ])
        
        return result
