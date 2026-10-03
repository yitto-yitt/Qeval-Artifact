# EVAL_META: task_id=139, framework=qpanda2, class=2
import pyqpanda as pq
import numpy as np

def schmidt_test(data, qargs_B):
    # Convert the input data to a density matrix if it's not already
    rho = np.array(data)
    
    # Get the total number of qubits
    n_qubits = int(np.log2(rho.shape[0]))
    
    # Determine qubits for partition A (complement of B)
    all_qubits = set(range(n_qubits))
    qargs_B_set = set(qargs_B)
    qargs_A = list(all_qubits - qargs_B_set)
    
    # Calculate the dimensions of each partition
    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    
    # Reshape the density matrix to perform SVD
    # Reshape to (dim_A, dim_B, dim_A, dim_B)
    reshaped_rho = rho.reshape(dim_A, dim_B, dim_A, dim_B)
    
    # Perform partial trace to get reduced density matrix for system A
    # Trace out system B
    reduced_rho_A = np.trace(reshaped_rho, axis1=1, axis2=3)
    
    # Perform eigenvalue decomposition on reduced density matrix
    eigenvals_A, eigenvecs_A = np.linalg.eigh(reduced_rho_A)
    
    # Only keep non-zero eigenvalues (with some tolerance for numerical errors)
    tol = 1e-12
    nonzero_indices = np.where(eigenvals_A > tol)[0]
    
    schmidt_terms = []
    
    for idx in nonzero_indices:
        # Schmidt coefficient is the square root of the eigenvalue
        schmidt_coeff = np.sqrt(max(0, eigenvals_A[idx]))  # max to avoid sqrt of small negative numbers
        
        # Eigenvector for subsystem A
        psi_A = eigenvecs_A[:, idx]
        
        # Calculate corresponding state for subsystem B
        # We need to use the original density matrix to find the corresponding B state
        # This requires more complex reconstruction from the full state
        # For a pure state |psi> = sum_i c_i |a_i> ⊗ |b_i>, where c_i are Schmidt coeffs
        
        # Reshape eigenvector back to match the tensor product structure
        psi_A_reshaped = psi_A.reshape((-1,))
        
        # Reconstruct the B state based on the original density matrix structure
        # Since we have rho = |psi><psi|, we can extract the components
        # For pure states, the density matrix has special structure
        
        # If the input represents a pure state density matrix |psi><psi|,
        # we can find the corresponding B state by looking at how A state couples with B state
        # in the original state vector before squaring
        
        # For this implementation, let's calculate the corresponding B state
        # by using the fact that the original state can be written as:
        # |psi> = sum_j sqrt(lambda_j) |u_j>_A ⊗ |v_j>_B
        # where |u_j> and |v_j> are the left and right singular vectors
        
        # Extract the original state vector from the density matrix (if it represents a pure state)
        # Find the eigenvalue decomposition of the full density matrix
        full_eigenvals, full_eigenvecs = np.linalg.eigh(rho)
        
        # Find the dominant eigenvalue (for pure state, there should be only one non-zero eigenvalue ~ 1.0)
        dominant_idx = np.argmax(full_eigenvals)
        if abs(full_eigenvals[dominant_idx] - 1.0) < 1e-6:  # Pure state
            # The dominant eigenvector is the state vector
            state_vector = full_eigenvecs[:, dominant_idx]
            
            # Reshape to tensor product form (dim_A, dim_B)
            state_tensor = state_vector.reshape(dim_A, dim_B)
            
            # Now project onto the A state to get the corresponding B state
            # <u_j|psi> = sum_i u_j*(i) * psi(i, :)
            # This gives us the corresponding B state up to normalization
            b_state_unnormalized = np.dot(psi_A.conj().T, state_tensor)
            
            # Normalize the B state
            norm_b = np.linalg.norm(b_state_unnormalized)
            if norm_b > 1e-12:
                psi_B = b_state_unnormalized / norm_b
            else:
                psi_B = np.zeros_like(b_state_unnormalized)
                psi_B[0] = 1.0  # Default normalized state if zero
            
            # Adjust the Schmidt coefficient if needed based on normalization
            # The coefficient might need adjustment based on the actual overlap
            # But for pure states in Schmidt form, the above approach should work
        else:
            # For mixed states, we can't directly get the B state from this method
            # In case of mixed state, the Schmidt decomposition is more complex
            # Let's create a default normalized B state
            psi_B = np.zeros(dim_B)
            psi_B[0] = 1.0
        
        schmidt_terms.append([schmidt_coeff, psi_A.tolist(), psi_B.tolist()])
    
    return schmidt_terms
