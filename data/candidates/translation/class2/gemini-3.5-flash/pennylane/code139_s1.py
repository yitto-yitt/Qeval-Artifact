# EVAL_META: task_id=139, framework=pennylane, class=2
import pennylane as qml
import numpy as np

def schmidt_test(data, qargs_B):
    # Convert data to numpy array
    data_np = qml.math.toarray(data)
    
    # Get state vector
    if len(data_np.shape) == 1:
        psi = data_np
    elif len(data_np.shape) == 2:
        # Density matrix
        evals, evecs = np.linalg.eigh(data_np)
        psi = evecs[:, -1]
    else:
        raise ValueError("Input data must be 1D or 2D.")
        
    N = int(round(np.log2(len(psi))))
    qargs_B = list(qargs_B)
    qargs_A = [i for i in range(N) if i not in qargs_B]
    
    tensor = np.reshape(psi, (2,) * N)
    
    axes_A = [N - 1 - i for i in reversed(qargs_A)]
    axes_B = [N - 1 - i for i in reversed(qargs_B)]
    
    transposed = np.transpose(tensor, axes_A + axes_B)
    
    dim_A = 2**len(qargs_A)
    dim_B = 2**len(qargs_B)
    matrix = np.reshape(transposed, (dim_A, dim_B))
    
    U, s, Vh = np.linalg.svd(matrix, full_matrices=False)
    
    components = []
    for i in range(len(s)):
        components.append((s[i], U[:, i], Vh[i, :]))
        
    return components
