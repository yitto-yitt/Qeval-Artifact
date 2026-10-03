# EVAL_META: task_id=139, framework=qpanda2, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    # Convert input to numpy array
    if hasattr(data, 'data'):
        state = np.asarray(data.data)
    else:
        state = np.asarray(data)
    
    # Get number of qubits
    n = int(np.round(np.log2(len(state))))
    
    # Reshape to multi-qubit tensor
    tensor = state.reshape([2] * n)
    
    # Identify qubits for A and B
    qargs_B = list(qargs_B)
    qargs_A = [i for i in range(n) if i not in qargs_B]
    
    # Map qubit indices to tensor axes (Qiskit big-endian mapping)
    axes_A = [n - 1 - k for k in reversed(sorted(qargs_A))]
    axes_B = [n - 1 - k for k in reversed(sorted(qargs_B))]
    
    # Transpose tensor to group A axes first, then B axes
    transposed_tensor = np.transpose(tensor, axes_A + axes_B)
    
    # Reshape to 2D matrix
    matrix = transposed_tensor.reshape(2**len(qargs_A), 2**len(qargs_B))
    
    # Perform SVD
    U, S, Vt = np.linalg.svd(matrix, full_matrices=False)
    
    # Create the list of results
    results = []
    for i in range(len(S)):
        results.append((S[i], U[:, i], Vt[i, :]))
        
    return results
