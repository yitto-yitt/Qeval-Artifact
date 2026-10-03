# EVAL_META: task_id=139, framework=pennylane, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    data = np.array(data)
    if data.ndim == 2:
        evals, evecs = np.linalg.eigh(data)
        idx = np.argmax(evals)
        state = evecs[:, idx]
    else:
        state = data
        
    N = int(np.round(np.log2(len(state))))
    qargs_B = list(qargs_B)
    qargs_A = [i for i in range(N) if i not in qargs_B]
    
    tensor = state.reshape([2] * N)
    
    axes_A = [N - 1 - q for q in qargs_A]
    axes_B = [N - 1 - q for q in qargs_B]
    
    tensor = np.transpose(tensor, axes_A + axes_B)
    
    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    matrix = tensor.reshape((dim_A, dim_B))
    
    U, S, Vh = np.linalg.svd(matrix, full_matrices=False)
    
    terms = []
    for i in range(len(S)):
        if S[i] > 1e-12:
            terms.append((float(S[i]), U[:, i], Vh[i, :]))
            
    return terms
