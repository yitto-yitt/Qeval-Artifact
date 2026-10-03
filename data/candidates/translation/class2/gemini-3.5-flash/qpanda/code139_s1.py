# EVAL_META: task_id=139, framework=qpanda, class=2
import numpy as np
import pyqpanda3.core as pq

def schmidt_test(data, qargs_B):
    if hasattr(data, 'data'):
        state = np.array(data.data)
    else:
        state = np.array(data)
    
    n_qubits = int(np.log2(len(state)))
    
    axes_B = [n_qubits - 1 - q for q in qargs_B]
    axes_A = [n_qubits - 1 - q for q in range(n_qubits) if q not in qargs_B]
    
    tensor = state.reshape([2] * n_qubits)
    
    perm = axes_A + axes_B
    transposed = np.transpose(tensor, perm)
    
    dim_A = 2 ** len(axes_A)
    dim_B = 2 ** len(axes_B)
    matrix = transposed.reshape((dim_A, dim_B))
    
    U, S, Vt = np.linalg.svd(matrix, full_matrices=False)
    
    atol = 1e-9
    rtol = 1e-9
    limit = rtol * S[0] + atol
    
    results = []
    for i in range(len(S)):
        if S[i] > limit:
            results.append((S[i], U[:, i], Vt[i, :]))
            
    return results
