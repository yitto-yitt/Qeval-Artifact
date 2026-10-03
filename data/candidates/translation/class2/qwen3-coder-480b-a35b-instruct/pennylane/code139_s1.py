# EVAL_META: task_id=139, framework=pennylane, class=2
import pennylane as qml
import numpy as np
from scipy.linalg import svd

def schmidt_test(data, qargs_B):
    # Convert to numpy array if needed
    rho = np.array(data)
    
    # Get total number of qubits
    n_qubits = int(np.log2(rho.shape[0]))
    
    # Determine qargs_A (complement of qargs_B)
    all_qubits = set(range(n_qubits))
    qargs_B_set = set(qargs_B)
    qargs_A = sorted(list(all_qubits - qargs_B_set))
    
    # Calculate dimensions
    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    
    # Reshape density matrix for SVD
    # We need to rearrange indices to group A and B subsystems
    perm = qargs_A + qargs_B
    inverse_perm = [0] * n_qubits
    for i, p in enumerate(perm):
        inverse_perm[p] = i
    
    # Reshape to combine subsystems
    rho_reshaped = rho.reshape([2] * 2 * n_qubits)
    rho_permuted = np.transpose(rho_reshaped, perm + [p + n_qubits for p in perm])
    rho_matrix = rho_permuted.reshape(dim_A, dim_B, dim_A, dim_B)
    
    # For Schmidt decomposition, we need the pure state case
    # Trace out subsystem B to get reduced density matrix for A
    rho_A = np.trace(rho_matrix, axis1=1, axis2=3)
    
    # Reshape to matrix form for SVD
    rho_A_matrix = rho_A.reshape(dim_A, dim_A)
    
    # But actually we should do SVD on the state vector if it's pure
    # For a general density matrix approach, we compute the SVD of the reshaped matrix
    # Reshape the original density matrix differently for bipartite splitting
    rho_bipartite = rho.reshape(dim_A, dim_B, dim_A, dim_B)
    # Take the partial trace to get reduced density matrices
    rho_A_red = np.trace(rho_bipartite, axis1=1, axis2=3) 
    rho_B_red = np.trace(rho_bipartite, axis1=0, axis2=2)
    
    # For pure states, we can work with the state vector directly
    # But since we have a density matrix, let's use the approach of reshaping
    # the density matrix and doing SVD on that
    rho_flat = rho.reshape(dim_A * dim_B, dim_A * dim_B)
    
    # If the state is pure, rho^2 = rho, so tr(rho^2) = 1
    # In that case we can find the state vector as the eigenvector with eigenvalue 1
    if abs(np.trace(rho_flat @ rho_flat) - 1.0) < 1e-10:
        # Pure state case
        eigenvals, eigenvecs = np.linalg.eigh(rho_flat)
        psi = eigenvecs[:, -1]  # Eigenvector corresponding to largest eigenvalue (should be 1)
        psi_normalized = psi / np.linalg.norm(psi)
        
        # Reshape to bipartite structure
        psi_bipartite = psi_normalized.reshape(dim_A, dim_B)
        
        # Perform SVD
        U, s, Vh = svd(psi_bipartite, full_matrices=False)
        
        # Construct result
        result = []
        for i in range(len(s)):
            if s[i] > 1e-12:  # Only include significant coefficients
                coeff = s[i]
                state_A = U[:, i]
                state_B = Vh[i, :].conj()
                result.append((coeff, state_A, state_B))
                
        return result
    else:
        # Mixed state case - use the general approach
        # This is more complex and would require a different treatment
        # For now, we'll implement the pure state version which matches typical usage
        raise NotImplementedError("Mixed state Schmidt decomposition not implemented")
