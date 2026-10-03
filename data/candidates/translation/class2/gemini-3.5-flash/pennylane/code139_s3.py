# EVAL_META: task_id=139, framework=pennylane, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    if isinstance(qargs_B, int):
        qargs_B = [qargs_B]
        
    state = np.array(data)
    N = int(np.round(np.log2(len(state))))
    
    qargs_A = [i for i in range(N) if i not in qargs_B]
    
    tensor = state.reshape([2] * N)
    
    axes_A = [N - 1 - i for i in reversed(qargs_A)]
    axes_B = [N - 1 - i for i in reversed(qargs_B)]
    
    perm = axes_A + axes_B
    tensor_perm = np.transpose(tensor, perm)
    
    matrix = tensor_perm.reshape(2**len(qargs_A), 2**len(qargs_B))
    
    U, S, Vt = np.linalg.svd(matrix, full_matrices=False)
    
    results = []
    for i in range(len(S)):
        results.append((S[i], U[:, i], Vt[i, :]))
        
    return results
