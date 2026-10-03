# EVAL_META: task_id=139, framework=pennylane, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    # Convert data to numpy array
    state = np.array(data)
    
    # If the input is a density matrix (2D), extract the state vector
    if state.ndim == 2:
        eigenvalues, eigenvectors = np.linalg.eigh(state)
        idx = np.argmax(eigenvalues)
        state = eigenvectors[:, idx]
        
    # Calculate number of qubits
    N = int(np.round(np.log2(len(state))))
    
    # Determine the qubits for subsystem A
    qargs_B = list(qargs_B)
    qargs_A = [i for i in range(N) if i not in qargs_B]
    
    # Map qubit indices to tensor axes.
    # In little-endian layout, qubit k corresponds to axis N - 1 - k.
    axes_A = [N - 1 - k for k in qargs_A]
    axes_B = [N - 1 - k for k in qargs_B]
    
    # Reshape state vector to tensor of shape (2, 2, ..., 2)
    tensor = np.reshape(state, [2] * N)
    
    # Transpose tensor to group subsystem A axes first, then subsystem B axes
    perm = axes_A + axes_B
    tensor_transposed = np.transpose(tensor, perm)
    
    # Reshape to a matrix of shape (2**len(qargs_A), 2**len(qargs_B))
    matrix = np.reshape(tensor_transposed, (2**len(qargs_A), 2**len(qargs_B)))
    
    # Perform Singular Value Decomposition
    U, s, Vh = np.linalg.svd(matrix, full_matrices=False)
    
    # Filter out terms with zero (or very small) coefficients
    tol = 1e-10
    schmidt_terms = []
    for i in range(len(s)):
        if s[i] > tol:
            schmidt_terms.append((s[i], U[:, i], Vh[i, :]))
            
    return schmidt_terms
