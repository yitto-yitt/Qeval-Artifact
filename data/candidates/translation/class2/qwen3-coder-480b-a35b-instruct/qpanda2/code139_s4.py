# EVAL_META: task_id=139, framework=qpanda2, class=2
import pyqpanda as pq
import numpy as np

def schmidt_test(data, qargs_B):
    # Convert the input data to a density matrix if it's not already
    rho = np.array(data)
    
    # Get total number of qubits
    n_qubits = int(np.log2(rho.shape[0]))
    
    # Define qubits for partition A and B
    all_qubits = list(range(n_qubits))
    qargs_A = [i for i in all_qubits if i not in qargs_B]
    
    # Perform SVD on the reshaped matrix to get Schmidt decomposition
    # Reshape the density matrix to matrix form for bipartite system
    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    
    # Reshape the matrix to (dim_A * dim_B) x (dim_A * dim_B)
    # Then we need to reshape appropriately to perform Schmidt decomposition
    
    # For pure states, we would work with the state vector
    # But since we have a density matrix, we may need to diagonalize it first
    # to find the eigenvalues and eigenvectors
    
    eigenvals, eigenvecs = np.linalg.eigh(rho)
    # Take only non-zero eigenvalues
    idx = np.where(eigenvals > 1e-12)[0]
    eigenvals = eigenvals[idx]
    eigenvecs = eigenvecs[:, idx]
    
    # For each eigenstate, we can compute its Schmidt decomposition
    results = []
    
    # If the density matrix represents a mixed state, 
    # the Schmidt decomposition is more complex
    # For now, let's assume it's a pure state represented by a vector
    # or handle the general case by considering the purification
    
    # If the input is a state vector instead of a density matrix
    if rho.ndim == 1 or rho.shape[0] == rho.shape[1] and np.allclose(rho @ rho, rho):  # Pure state check
        if rho.ndim == 2:
            # Extract the state vector from the density matrix (assuming pure state)
            psi = eigenvecs[:, -1] * np.sqrt(eigenvals[-1])  # Take the dominant eigenstate
        else:
            psi = rho.flatten()
        
        # Reshape the state vector to the tensor product space
        psi_reshaped = psi.reshape((dim_A, dim_B))
        
        # Perform SVD to get Schmidt decomposition
        U, schmidt_coeffs, Vh = np.linalg.svd(psi_reshaped)
        
        # Normalize the coefficients
        schmidt_coeffs = np.sqrt(np.abs(schmidt_coeffs))  # Square root because svd gives squared values
        
        for i in range(len(schmidt_coeffs)):
            if schmidt_coeffs[i] > 1e-12:  # Only include non-negligible coefficients
                subsystem_A = U[:, i]
                subsystem_B = Vh[i, :]  # Vh is already conjugate transposed
                results.append([schmidt_coeffs[i], subsystem_A.tolist(), subsystem_B.tolist()])
    else:
        # For mixed states, the decomposition is more complex
        # We'll treat the eigenvalues as probabilities and eigenvectors as pure states
        for i in range(len(eigenvals)):
            if eigenvals[i] > 1e-12:
                psi = eigenvecs[:, i]
                # Reshape the state vector to the tensor product space
                psi_reshaped = psi.reshape((dim_A, dim_B))
                
                # Perform SVD to get Schmidt decomposition
                U, s_coeffs, Vh = np.linalg.svd(psi_reshaped)
                
                # For mixed states, we take sqrt of eigenvalue as amplitude
                amplitude = np.sqrt(eigenvals[i])
                
                # Add the contribution from this eigenstate
                for j in range(len(s_coeffs)):
                    if s_coeffs[j] > 1e-12:
                        coeff = amplitude * np.sqrt(s_coeffs[j])  # Combined amplitude
                        subsystem_A = U[:, j]
                        subsystem_B = Vh[j, :]
                        results.append([coeff, subsystem_A.tolist(), subsystem_B.tolist()])
    
    return results
