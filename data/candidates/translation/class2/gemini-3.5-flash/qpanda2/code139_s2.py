# EVAL_META: task_id=139, framework=qpanda2, class=2
import numpy as np
import pyqpanda as pq

def schmidt_test(data, qargs_B):
    if hasattr(data, 'data'):
        state = np.asarray(data.data)
    else:
        state = np.asarray(data)
    
    n_qubits = int(np.round(np.log2(len(state))))
    
    try:
        qargs_B = list(qargs_B)
    except TypeError:
        qargs_B = [qargs_B]
        
    qargs_A = [i for i in range(n_qubits) if i not in qargs_B]
    
    axes_A = [n_qubits - 1 - i for i in qargs_A]
    axes_B = [n_qubits - 1 - i for i in qargs_B]
    
    tensor = state.reshape([2] * n_qubits)
    perm = axes_A + axes_B
    tensor_perm = np.transpose(tensor, perm)
    
    dim_A = 2**len(qargs_A)
    dim_B = 2**len(qargs_B)
    matrix = tensor_perm.reshape((dim_A, dim_B))
    
    U, S, Vh = np.linalg.svd(matrix, full_matrices=False)
    
    results = []
    for i in range(len(S)):
        results.append((S[i], U[:, i], Vh[i, :]))
        
    return results
