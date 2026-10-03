# EVAL_META: task_id=139, framework=qpanda2, class=2
import pyqpanda as pq
import numpy as np

def schmidt_test(data, qargs_B):
    # Convert the input data to a density matrix if it's not already
    rho = np.array(data)
    
    # Get the total number of qubits
    n_qubits = int(np.log2(rho.shape[0]))
    
    # Determine qubits for subsystem A (complement of qargs_B)
    all_qubits = set(range(n_qubits))
    qargs_B_set = set(qargs_B)
    qargs_A = sorted(list(all_qubits - qargs_B_set))
    
    # Perform SVD on the reshaped matrix to get Schmidt decomposition
    # Reshape the density matrix to matrix form for bipartite system
    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    
    # Reshape the density matrix appropriately
    reshaped_matrix = rho.reshape(dim_A, dim_B, dim_A, dim_B)
    
    # For pure states represented as vectors, we need different handling
    # Check if data represents a state vector or density matrix
    if len(rho.shape) == 1 or rho.shape[0] == rho.shape[1]:
        # This is likely a density matrix, but for Schmidt decomp we may need the state vector
        # If it's a pure state density matrix, find its rank-1 decomposition
        eigenvals, eigenvecs = np.linalg.eigh(rho)
        
        # Find the non-zero eigenvalue and corresponding eigenvector (for pure state)
        max_eigenval_idx = np.argmax(eigenvals)
        psi = eigenvecs[:, max_eigenval_idx]
        
        # Reshape the state vector according to the partition
        psi_reshaped = psi.reshape((2**len(qargs_A), 2**len(qargs_B)))
        
        # Perform SVD to get Schmidt decomposition
        U, singular_vals, Vh = np.linalg.svd(psi_reshaped)
        
        # Create the result list with coefficients, subsystem A states, and subsystem B states
        result = []
        for i in range(len(singular_vals)):
            coeff = singular_vals[i]
            state_A = U[:, i].tolist()
            state_B = Vh[i, :].tolist()  # Vh is already conjugated transpose
            result.append([coeff, state_A, state_B])
            
        return result
    else:
        # If it's already a state vector
        psi = np.array(data).flatten()
        psi_reshaped = psi.reshape((2**len(qargs_A), 2**len(qargs_B)))
        
        # Perform SVD to get Schmidt decomposition
        U, singular_vals, Vh = np.linalg.svd(psi_reshaped)
        
        # Create the result list with coefficients, subsystem A states, and subsystem B states
        result = []
        for i in range(len(singular_vals)):
            coeff = singular_vals[i]
            state_A = U[:, i].tolist()
            state_B = Vh[i, :].tolist()  # Vh is already conjugated transpose
            result.append([coeff, state_A, state_B])
            
        return result
