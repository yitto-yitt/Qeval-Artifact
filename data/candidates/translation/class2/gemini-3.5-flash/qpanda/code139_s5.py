# EVAL_META: task_id=139, framework=qpanda, class=2
import numpy as np
import pyqpanda3

def schmidt_test(data, qargs_B):
    if hasattr(data, 'data'):
        state = np.asarray(data.data)
    else:
        state = np.asarray(data)
        
    n = int(np.log2(len(state)))
    
    if isinstance(qargs_B, int):
        qargs_B = [qargs_B]
    else:
        qargs_B = list(qargs_B)
        
    qargs_A = [i for i in range(n) if i not in qargs_B]
    
    axes_A = [n - 1 - i for i in reversed(qargs_A)]
    axes_B = [n - 1 - i for i in reversed(qargs_B)]
    
    tensor = state.reshape([2] * n)
    perm = axes_A + axes_B
    tensor_perm = np.transpose(tensor, perm)
    
    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    matrix = tensor_perm.reshape((dim_A, dim_B))
    
    U, S, Vh = np.linalg.svd(matrix, full_matrices=False)
    
    results = []
    for k in range(len(S)):
        coeff = S[k]
        state_A = U[:, k]
        state_B = Vh[k, :]
        results.append((coeff, state_A, state_B))
        
    return results
