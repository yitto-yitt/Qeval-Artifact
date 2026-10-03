# EVAL_META: task_id=139, framework=qpanda2, class=2
import pyqpanda as pq
import numpy as np

def schmidt_test(data, qargs_B):
    # Convert the input data to a density matrix if it's not already
    rho = np.array(data)
    
    # Get total number of qubits
    n_qubits = int(np.log2(rho.shape[0]))
    qubits_A = [i for i in range(n_qubits) if i not in qargs_B]
    
    # Calculate the reduced density matrix for subsystem A
    # Trace out subsystem B
    rho_A = partial_trace(rho, qargs_B, n_qubits)
    
    # Perform eigenvalue decomposition on the reduced density matrix
    eigenvals, eigenvecs = np.linalg.eigh(rho_A)
    
    # Sort in descending order (Schmidt coefficients are square roots of eigenvalues)
    idx = np.argsort(eigenvals)[::-1]
    eigenvals = eigenvals[idx]
    eigenvecs = eigenvecs[:, idx]
    
    # Schmidt coefficients are square roots of the eigenvalues
    schmidt_coeffs = np.sqrt(np.maximum(eigenvals, 0))  # Avoid negative values due to numerical errors
    
    # Prepare results
    results = []
    for i in range(len(schmidt_coeffs)):
        if schmidt_coeffs[i] > 1e-10:  # Only include non-zero coefficients
            coeff = schmidt_coeffs[i]
            
            # Get the corresponding eigenvector for subsystem A
            psi_A = eigenvecs[:, i]
            
            # For subsystem B, we need to find the corresponding state
            # This requires more complex calculations involving the original state
            # For now, we'll use the structure of the Schmidt decomposition
            
            # In the Schmidt decomposition |psi> = sum_k lambda_k |phi_k^A> |phi_k^B>
            # where |phi_k^A> and |phi_k^B> are orthonormal basis states for subsystems A and B
            
            # Since we have the reduced density matrix, we can't directly get the B part
            # without the full state information. However, we can create placeholder states
            # based on the decomposition principles.
            
            # Create subsystem states
            psi_B = construct_subsystem_B_state(rho, psi_A, qubits_A, qargs_B)
            
            results.append([coeff, psi_A.tolist(), psi_B.tolist()])
    
    return results

def partial_trace(rho, qubits_to_trace_out, total_qubits):
    """Calculate the partial trace of a density matrix"""
    dim_A = 2 ** (total_qubits - len(qubits_to_trace_out))
    dim_B = 2 ** len(qubits_to_trace_out)
    
    # Reshape the density matrix to tensor form
    rho_tensor = rho.reshape([2] * total_qubits * 2)
    
    # Permute axes to group traced-out qubits together
    all_qubits = list(range(total_qubits))
    remaining_qubits = [i for i in all_qubits if i not in qubits_to_trace_out]
    
    # Create axis orderings
    left_axes = remaining_qubits + [i + total_qubits for i in remaining_qubits]
    right_axes = qubits_to_trace_out + [i + total_qubits for i in qubits_to_trace_out]
    
    # Rearrange the tensor to separate the qubits to trace out
    axes_order = remaining_qubits + qubits_to_trace_out + \
                 [i + total_qubits for i in remaining_qubits] + [i + total_qubits for i in qubits_to_trace_out]
    
    rho_tensor = rho_tensor.transpose(axes_order)
    
    # Reshape to separate dimensions
    rho_tensor = rho_tensor.reshape((dim_A, dim_B, dim_A, dim_B))
    
    # Take the trace over the B subsystem
    rho_reduced = np.trace(rho_tensor, axis1=1, axis2=3)
    
    return rho_reduced

def construct_subsystem_B_state(full_state, state_A, qubits_A, qubits_B):
    """Construct the B subsystem state corresponding to state A in Schmidt decomposition"""
    # This is a simplified approach; a full implementation would require 
    # reconstructing the full bipartite state if available
    
    # If the input is a pure state vector
    if len(full_state.shape) == 1:
        n_total = len(full_state)
        n_qubits = int(np.log2(n_total))
        
        # Reshape the full state into a matrix form where rows correspond to A and columns to B
        dim_A = len(state_A)
        dim_B = n_total // dim_A
        
        state_matrix = full_state.reshape((dim_A, dim_B))
        
        # Compute the B state corresponding to the A state
        # This involves finding the projection onto the A state
        state_B = np.dot(state_A.conj().T, state_matrix)
        norm = np.linalg.norm(state_B)
        if norm > 1e-10:
            state_B = state_B / norm
        else:
            # Default to first computational basis state if norm is too small
            state_B = np.zeros(dim_B)
            state_B[0] = 1.0
            
        return state_B
    else:
        # For mixed states, we can't uniquely determine the B state from just the reduced density matrix
        # We return a normalized vector of appropriate size
        dim_B = 2 ** len(qubits_B)
        state_B = np.zeros(dim_B)
        state_B[0] = 1.0
        return state_B
