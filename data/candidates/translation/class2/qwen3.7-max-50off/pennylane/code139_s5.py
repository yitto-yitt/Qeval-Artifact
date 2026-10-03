# EVAL_META: task_id=139, framework=pennylane, class=2
import numpy as np
import pennylane as qml

def schmidt_test(data, qargs_B):
    data = np.array(data)
    if data.ndim == 2:
        evals, evecs = np.linalg.eigh(data)
        idx = np.argmax(evals)
        state = evecs[:, idx]
    else:
        state = data
        
    N = int(np.round(np.log2(state.shape[0])))
    qargs_B = list(qargs_B)
    axes_A = [i for i in range(N) if i not in qargs_B]
    
    tensor = state.reshape([2] * N)
    tensor = np.transpose(tensor, axes_A + qargs_B)
    
    dim_A = 2 ** len(axes_A)
    dim_B = 2 ** len(qargs_B)
    matrix = tensor.reshape((dim_A, dim_B))
    
    U, S, Vh = np.linalg.svd(matrix, full_matrices=False)
    
    terms = []
    for k in range(len(S)):
        if S[k] > 1e-10:
            terms.append((float(S[k]), U[:, k], Vh[k, :]))
            
    return terms
