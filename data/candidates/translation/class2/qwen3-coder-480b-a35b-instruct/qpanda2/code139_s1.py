# EVAL_META: task_id=139, framework=qpanda2, class=2
import pyqpanda as pq
import numpy as np

def schmidt_test(data, qargs_B):
    # Convert the input data to a density matrix if it's not already
    rho = np.array(data)
    
    # Get total number of qubits
    n_qubits = int(np.log2(rho.shape[0]))
    
    # Define qubits for subsystem A based on qargs_B
    all_qubits = list(range(n_qubits))
    qargs_A = [q for q in all_qubits if q not in qargs_B]
    
    # Calculate dimensions of subsystems
    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    
    # Reshape the density matrix to matrix form if needed
    if rho.ndim == 1:
        # If data is a state vector, convert to density matrix first
        psi = rho
        rho = np.outer(psi, np.conj(psi))
    
    # Perform SVD on the reshaped matrix to get Schmidt decomposition
    # Reshape the density matrix to a matrix where rows correspond to A and columns to B
    reshaped_matrix = rho.reshape(dim_A, dim_B)
    
    # Compute SVD
    U, singular_values, Vh = np.linalg.svd(reshaped_matrix)
    
    # Prepare results
    result = []
    for i in range(len(singular_values)):
        coefficient = singular_values[i]
        state_A = U[:, i]  # State vector for subsystem A
        state_B = Vh[i, :]  # State vector for subsystem B
        
        result.append([coefficient, state_A.tolist(), state_B.tolist()])
    
    return result
