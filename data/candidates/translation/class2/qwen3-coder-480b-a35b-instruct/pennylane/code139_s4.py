# EVAL_META: task_id=139, framework=pennylane, class=2
import pennylane as qml
from pennylane import numpy as np

def schmidt_test(data, qargs_B):
    # Convert the input data to a numpy array if it's not already
    rho = np.array(data)
    
    # Get the dimensions
    dim_total = rho.shape[0]
    n_qubits = int(np.log2(dim_total))
    
    # Determine subsystem A indices
    all_qubits = set(range(n_qubits))
    qargs_A = sorted(list(all_qubits - set(qargs_B)))
    
    # Reshape the density matrix to perform SVD
    # Reshape rho into a 4D tensor: (dim_A, dim_B, dim_A, dim_B)
    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    
    # We need to rearrange the axes to group A and B subsystems together
    # First reshape to (2, 2, ..., 2) for each qubit
    reshaped_rho = rho.reshape([2] * n_qubits + [2] * n_qubits)
    
    # Rearrange axes so that all A qubits come first, then B qubits
    axes_A_first = qargs_A + [x + n_qubits for x in qargs_A]
    axes_B_next = qargs_B + [x + n_qubits for x in qargs_B]
    all_axes = axes_A_first + axes_B_next
    
    # Transpose the tensor according to our desired ordering
    transposed_rho = np.transpose(reshaped_rho, all_axes)
    
    # Reshape to (dim_A*dim_A, dim_B*dim_B)
    reshaped_for_svd = transposed_rho.reshape((dim_A * dim_A, dim_B * dim_B))
    
    # Perform SVD on the reshaped matrix
    U, s, Vh = np.linalg.svd(reshaped_for_svd)
    
    # The singular values are the square roots of the Schmidt coefficients
    schmidt_coeffs = np.sqrt(s)
    
    # Filter out negligible coefficients
    threshold = 1e-8
    significant_indices = np.where(schmidt_coeffs > threshold)[0]
    
    result = []
    for idx in significant_indices:
        coeff = schmidt_coeffs[idx]
        
        # Extract the corresponding vectors for subsystem A and B
        # From U, extract the vector for subsystem A
        u_vec = U[:, idx]
        # Reshape to get the state vector for subsystem A
        psi_A = u_vec.reshape((dim_A, 1))  # Shape (dim_A, 1)
        
        # From Vh, extract the vector for subsystem B  
        v_vec = Vh[idx, :]
        # Reshape to get the state vector for subsystem B
        psi_B = v_vec.reshape((dim_B, 1))  # Shape (dim_B, 1)
        
        result.append([coeff, psi_A.flatten(), psi_B.flatten()])
    
    return result
