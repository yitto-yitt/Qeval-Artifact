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
    # First, we need to determine the correct tensor contraction order
    rho_tensor = rho.reshape([2] * n_qubits + [2] * n_qubits)
    
    # Transpose to group A and B indices together
    axes_A_first = qargs_A + [n_qubits + i for i in qargs_A]
    axes_B_first = qargs_B + [n_qubits + i for i in qargs_B]
    all_axes = axes_A_first + axes_B_first
    
    # Reshape to matrix form for SVD
    rho_AB = rho_tensor.transpose(all_axes).reshape((dim_A * dim_A, dim_B * dim_B))
    
    # Perform SVD on the reshaped matrix to get the Schmidt decomposition
    U, s, Vh = np.linalg.svd(rho_AB)
    
    # Extract the Schmidt coefficients
    schmidt_coeffs = np.sqrt(s)  # For pure states, but this works for the general case too
    
    # Normalize the coefficients so they sum to 1 (probabilities)
    schmidt_coeffs = schmidt_coeffs / np.sum(schmidt_coeffs**2)**0.5
    
    # Filter out very small coefficients
    threshold = 1e-8
    valid_indices = schmidt_coeffs > threshold
    
    result = []
    for i in range(len(schmidt_coeffs)):
        if valid_indices[i]:
            coeff = schmidt_coeffs[i]
            # Create the corresponding subsystem states
            state_A = U[:, i].reshape(dim_A)
            state_B = Vh[i, :].reshape(dim_B)
            
            # Normalize the states
            state_A = state_A / np.linalg.norm(state_A)
            state_B = state_B / np.linalg.norm(state_B)
            
            result.append([coeff, state_A.tolist(), state_B.tolist()])
    
    return result
