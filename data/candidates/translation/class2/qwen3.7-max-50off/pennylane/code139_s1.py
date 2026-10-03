# EVAL_META: task_id=139, framework=pennylane, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    data = np.asarray(data)
    if data.ndim == 2:
        if data.shape[1] == 1:
            data = data.flatten()
        elif data.shape[0] == data.shape[1]:
            eigvals, eigvecs = np.linalg.eigh(data)
            data = eigvecs[:, np.argmax(eigvals)]
            
    N = int(np.round(np.log2(data.shape[0])))
    
    qargs_A = sorted([q for q in range(N) if q not in qargs_B])
    qargs_B = sorted(qargs_B)
    
    axes_A = [N - 1 - q for q in qargs_A]
    axes_B = [N - 1 - q for q in qargs_B]
    
    tensor = data.reshape((2,) * N)
    tensor = np.transpose(tensor, axes_A + axes_B)
    
    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    
    matrix = tensor.reshape((dim_A, dim_B))
    
    U, S, Vh = np.linalg.svd(matrix, full_matrices=False)
    
    result = []
    for i in range(len(S)):
        if S[i] > 1e-12:
            result.append((float(S[i]), U[:, i], Vh[i, :]))
            
    return result
