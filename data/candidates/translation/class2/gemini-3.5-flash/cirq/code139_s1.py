# EVAL_META: task_id=139, framework=cirq, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    if hasattr(data, 'final_state_vector'):
        state_vector = data.final_state_vector
    elif hasattr(data, 'state_vector'):
        state_vector = data.state_vector() if callable(data.state_vector) else data.state_vector
    elif hasattr(data, 'data'):
        state_vector = data.data
    else:
        state_vector = np.asarray(data)
        
    if state_vector.ndim == 2:
        if state_vector.shape[1] == 1:
            state_vector = state_vector.ravel()
        elif state_vector.shape[0] == 1:
            state_vector = state_vector.ravel()
        else:
            evals, evecs = np.linalg.eigh(state_vector)
            state_vector = evecs[:, -1]
            
    N = int(np.round(np.log2(len(state_vector))))
    dims = (2,) * N
    qargs_A = [i for i in range(N) if i not in qargs_B]
    
    tensor = np.reshape(state_vector, dims)
    tensor = np.transpose(tensor, qargs_A + qargs_B)
    
    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    matrix = np.reshape(tensor, (dim_A, dim_B))
    
    U, S, Vh = np.linalg.svd(matrix, full_matrices=False)
    
    components = []
    for i in range(len(S)):
        if S[i] > 1e-9:
            components.append((S[i], U[:, i], Vh[i, :]))
            
    return components
