# EVAL_META: task_id=139, framework=qpanda, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    if hasattr(data, 'data'):
        state = np.array(data.data)
    elif hasattr(data, 'to_vector'):
        state = np.array(data.to_vector())
    else:
        state = np.array(data)
        
    if state.ndim > 1:
        state = state.ravel()
        
    n = int(np.log2(len(state)))
    dims = (2,) * n
    
    if isinstance(qargs_B, int):
        qargs_B = [qargs_B]
    else:
        qargs_B = list(qargs_B)
        
    qargs_A = [i for i in range(n) if i not in qargs_B]
    
    tensor = np.reshape(state, dims[::-1])
    
    axes_A = [n - 1 - i for i in reversed(qargs_A)]
    axes_B = [n - 1 - i for i in reversed(qargs_B)]
    
    tensor = np.transpose(tensor, axes_A + axes_B)
    
    dim_A = 2**len(qargs_A)
    dim_B = 2**len(qargs_B)
    matrix = np.reshape(tensor, (dim_A, dim_B))
    
    U, S, Vh = np.linalg.svd(matrix, full_matrices=False)
    
    results = []
    for k in range(len(S)):
        if S[k] > 1e-10:
            coeff = S[k]
            state_A = U[:, k]
            state_B = Vh[k, :]
            results.append((coeff, state_A, state_B))
            
    return results
