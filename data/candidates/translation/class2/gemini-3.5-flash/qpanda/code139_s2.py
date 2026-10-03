# EVAL_META: task_id=139, framework=qpanda, class=2
import numpy as np
import pyqpanda3.core as pq

def schmidt_test(data, qargs_B):
    if hasattr(data, 'data'):
        state = np.array(data.data)
    else:
        state = np.array(data)
        
    N = int(np.log2(len(state)))
    tensor = state.reshape([2] * N)
    
    qargs_A = [k for k in range(N) if k not in qargs_B]
    
    qargs_A_reversed = qargs_A[::-1]
    qargs_B_reversed = qargs_B[::-1]
    
    axes_A = [N - 1 - k for k in qargs_A_reversed]
    axes_B = [N - 1 - k for k in qargs_B_reversed]
    
    perm = axes_A + axes_B
    transposed = np.transpose(tensor, perm)
    
    matrix = transposed.reshape((2**len(qargs_A), 2**len(qargs_B)))
    
    U, S, Vt = np.linalg.svd(matrix, full_matrices=False)
    
    results = []
    for k in range(len(S)):
        if S[k] > 1e-9:
            results.append((S[k], U[:, k], Vt[k, :]))
    return results
