# EVAL_META: task_id=139, framework=qpanda2, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    if hasattr(data, 'data'):
        data = np.asarray(data.data, dtype=complex)
    else:
        data = np.asarray(data, dtype=complex)
        
    N = int(np.round(np.log2(data.shape[0])))
    qargs_A = [i for i in range(N) if i not in qargs_B]
    
    tensor = data.reshape([2] * N)
    axes = qargs_A + list(qargs_B)
    tensor = np.transpose(tensor, axes)
    
    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    matrix = tensor.reshape((dim_A, dim_B))
    
    U, S, Vh = np.linalg.svd(matrix, full_matrices=False)
    
    results = []
    for i in range(len(S)):
        if S[i] > 1e-10:
            results.append((float(S[i]), U[:, i], Vh[i, :]))
            
    return results
