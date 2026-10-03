# EVAL_META: task_id=139, framework=qpanda2, class=2
import numpy as np
import pyqpanda as pq

def schmidt_test(data, qargs_B):
    # Convert data to a 1D numpy array representing the state vector
    if hasattr(data, 'data'):
        state = np.asarray(data.data)
    elif hasattr(data, 'to_vector'):
        state = np.asarray(data.to_vector())
    else:
        state = np.asarray(data)
        
    n = int(np.log2(len(state)))
    
    # Extract integer indices for subsystem B
    q_indices_B = []
    for q in qargs_B:
        if hasattr(q, 'get_phy_addr'):
            q_indices_B.append(q.get_phy_addr())
        elif hasattr(q, 'index'):
            q_indices_B.append(q.index)
        else:
            q_indices_B.append(int(q))
            
    # Subsystem A consists of the remaining qubits
    qargs_A = [i for i in range(n) if i not in q_indices_B]
    
    # Map qubit indices to tensor axes (qubit i corresponds to axis n - 1 - i)
    axes_A = [n - 1 - i for i in qargs_A]
    axes_B = [n - 1 - i for i in q_indices_B]
    
    # Reshape and transpose the state tensor
    tensor = state.reshape([2] * n)
    tensor = np.transpose(tensor, axes_A + axes_B)
    
    # Reshape to a matrix for SVD
    matrix = tensor.reshape(2**len(qargs_A), 2**len(q_indices_B))
    
    # Perform SVD
    U, s, Vh = np.linalg.svd(matrix)
    
    # Return the Schmidt decomposition terms
    results = []
    for i in range(len(s)):
        results.append((s[i], U[:, i], Vh[i, :]))
        
    return results
