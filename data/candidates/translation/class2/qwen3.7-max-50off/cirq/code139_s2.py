# EVAL_META: task_id=139, framework=cirq, class=2
import numpy as np
import cirq

def schmidt_test(data, qargs_B):
    data = np.asarray(data, dtype=complex)
    if data.ndim == 2 and 1 in data.shape:
        data = data.flatten()
        
    N = int(np.round(np.log2(data.shape[0])))
    tensor = data.reshape([2] * N)
    
    if isinstance(qargs_B, int):
        qargs_B = [qargs_B]
        
    axes_B = [N - 1 - q for q in qargs_B]
    axes_A = [N - 1 - q for q in range(N) if q not in qargs_B]
    
    transposed = tensor.transpose(axes_A + axes_B)
    
    dim_A = 2 ** len(axes_A)
    dim_B = 2 ** len(axes_B)
    
    mat = transposed.reshape(dim_A, dim_B)
    
    U, S, Vh = np.linalg.svd(mat, full_matrices=False)
    
    result = []
    for i in range(len(S)):
        if S[i] > 1e-10:
            result.append((float(S[i]), U[:, i], Vh[i, :]))
            
    return result
