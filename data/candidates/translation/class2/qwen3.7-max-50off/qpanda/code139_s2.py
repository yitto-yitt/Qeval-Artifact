# EVAL_META: task_id=139, framework=qpanda, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    if hasattr(data, 'data'):
        state = np.array(data.data, dtype=complex)
    elif hasattr(data, 'to_matrix'):
        state = np.array(data.to_matrix(), dtype=complex)
    else:
        state = np.array(data, dtype=complex)
        
    if state.ndim == 2:
        evals, evecs = np.linalg.eigh(state)
        state = evecs[:, np.argmax(evals)]
        
    n = int(np.round(np.log2(len(state))))
    axes_B = [n - 1 - q for q in qargs_B]
    axes_A = [n - 1 - q for q in range(n) if q not in qargs_B]
    
    tensor = state.reshape((2,) * n)
    tensor = np.transpose(tensor, axes_A + axes_B)
    matrix = tensor.reshape((2**len(axes_A), 2**len(axes_B)))
    
    U, S, Vh = np.linalg.svd(matrix, full_matrices=False)
    
    result = []
    for i in range(len(S)):
        if S[i] > 1e-12:
            coeff = float(S[i])
            state_A = U[:, i]
            state_B = Vh[i, :].conj()
            result.append((coeff, state_A, state_B))
            
    return result
