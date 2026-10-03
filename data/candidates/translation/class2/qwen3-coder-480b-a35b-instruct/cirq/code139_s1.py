# EVAL_META: task_id=139, framework=cirq, class=2
import numpy as np
import cirq

def schmidt_test(data, qargs_B):
    # Convert input to numpy array if needed
    rho = np.array(data)
    
    # Determine total number of qubits
    n_qubits = int(np.log2(rho.shape[0]))
    
    # Determine qargs_A (complement of qargs_B)
    all_qubits = set(range(n_qubits))
    qargs_A = sorted(list(all_qubits - set(qargs_B)))
    
    # Calculate dimensions
    dim_A = 2**len(qargs_A)
    dim_B = 2**len(qargs_B)
    
    # Reshape density matrix for SVD
    # Group indices for subsystems A and B
    perm = qargs_A + qargs_B
    inv_perm = [0] * len(perm)
    for i, p in enumerate(perm):
        inv_perm[p] = i
    
    # Reshape and permute indices
    rho_reshaped = rho.reshape([2]*2*n_qubits)
    rho_permuted = np.transpose(rho_reshaped, inv_perm + [i+n_qubits for i in inv_perm])
    rho_matrix = rho_permuted.reshape(dim_A, dim_B, dim_A, dim_B)
    
    # Trace out to get reduced density matrices
    rho_A = np.trace(rho_matrix, axis1=1, axis2=3)
    rho_B = np.trace(rho_matrix, axis1=0, axis2=2)
    
    # Reshape for matrix form
    rho_AB_vec = rho_matrix.reshape(dim_A*dim_B, dim_A*dim_B)
    
    # Perform SVD on the reshaped density matrix
    U, s, Vh = np.linalg.svd(rho_AB_vec)
    
    # Extract Schmidt coefficients and states
    schmidt_coeffs = []
    for i in range(min(dim_A, dim_B)):
        if s[i] > 1e-10:  # Only include significant coefficients
            coeff = np.sqrt(s[i])
            state_A = U[:, i].reshape(dim_A)
            state_B = Vh[i, :].reshape(dim_B)
            schmidt_coeffs.append((coeff, state_A, state_B))
    
    return schmidt_coeffs
