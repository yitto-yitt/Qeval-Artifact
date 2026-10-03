# EVAL_META: task_id=139, framework=qpanda, class=2
import pyqpanda3.core as pq
import numpy as np

def schmidt_test(data, qargs_B):
    # Convert the input data to numpy array if it's not already
    density_matrix = np.array(data)
    
    # Get dimensions
    dim = density_matrix.shape[0]
    n_qubits = int(np.log2(dim))
    
    # Partition information
    qubits_A = [i for i in range(n_qubits) if i not in qargs_B]
    qubits_B = qargs_B
    
    # Calculate the dimensions of each subsystem
    dim_A = 2 ** len(qubits_A)
    dim_B = 2 ** len(qubits_B)
    
    # Reshape the density matrix to a bipartite state form if it's a pure state vector
    # Otherwise work with the density matrix directly
    if len(density_matrix.shape) == 1 or density_matrix.shape[0] == density_matrix.shape[1]:
        # Treat as density matrix - we need to find its eigenvalues and eigenvectors
        # For a pure state, the density matrix has rank 1, so we find the state first
        eigenvals, eigenvecs = np.linalg.eigh(density_matrix)
        
        # Find the non-zero eigenvalue (for pure states this should be one significant value ~1.0)
        # corresponding to the actual state
        max_eigenval_idx = np.argmax(eigenvals)
        psi = eigenvecs[:, max_eigenval_idx]
        
        # Reshape the state vector to the tensor product form |A> ⊗ |B>
        psi_reshaped = psi.reshape((dim_A, dim_B))
        
        # Perform SVD on the reshaped matrix to get Schmidt decomposition
        U, schmidt_coeffs, Vh = np.linalg.svd(psi_reshaped)
        
        # Prepare results
        results = []
        for i in range(len(schmidt_coeffs)):
            coeff = schmidt_coeffs[i]
            if abs(coeff) > 1e-10:  # Only include significant coefficients
                state_A = U[:, i]
                state_B = Vh[i, :]  # Note: Vh is already conjugated transpose
                results.append([coeff, state_A.tolist(), state_B.tolist()])
        
        return results
    else:
        # If it's a state vector directly
        psi = np.array(density_matrix).flatten()
        psi_reshaped = psi.reshape((dim_A, dim_B))
        
        # Perform SVD on the reshaped matrix to get Schmidt decomposition
        U, schmidt_coeffs, Vh = np.linalg.svd(psi_reshaped)
        
        # Prepare results
        results = []
        for i in range(len(schmidt_coeffs)):
            coeff = schmidt_coeffs[i]
            if abs(coeff) > 1e-10:  # Only include significant coefficients
                state_A = U[:, i]
                state_B = Vh[i, :]  # Note: Vh is already conjugated transpose
                results.append([coeff, state_A.tolist(), state_B.tolist()])
        
        return results
