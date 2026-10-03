# EVAL_META: task_id=139, framework=pennylane, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    # Convert input to a statevector
    data = np.asarray(data)
    if data.ndim == 2:
        # If it's a density matrix, find the statevector corresponding to the largest eigenvalue
        eigenvalues, eigenvectors = np.linalg.eigh(data)
        psi = eigenvectors[:, -1]
    else:
        psi = data
        
    N = int(np.log2(len(psi)))
    
    if isinstance(qargs_B, int):
        qargs_B = [qargs_B]
    else:
        qargs_B = sorted(list(qargs_B))
        
    qargs_A = sorted([i for i in range(N) if i not in qargs_B])
    
    axes_A = [N - 1 - i for i in reversed(qargs_A)]
    axes_B = [N - 1 - i for i in reversed(qargs_B)]
    
    tensor = np.reshape(psi, [2] * N)
    perm = axes_A + axes_B
    tensor_transposed = np.transpose(tensor, perm)
    
    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    matrix = np.reshape(tensor_transposed, (dim_A, dim_B))
    
    U, S, Vh = np.linalg.svd(matrix)
    
    results = []
    for i in range(len(S)):
        coeff = S[i]
        state_A = U[:, i]
        state_B = Vh[i, :]
        results.append((coeff, state_A, state_B))
        
    return results
