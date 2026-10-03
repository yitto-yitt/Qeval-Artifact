# EVAL_META: task_id=139, framework=cirq, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    data = np.asarray(data).flatten()
    N = int(np.round(np.log2(len(data))))
    
    qargs_A = [i for i in range(N) if i not in qargs_B]
    
    qargs_A_sorted = sorted(qargs_A, reverse=True)
    qargs_B_sorted = sorted(qargs_B, reverse=True)
    
    axes_A = [N - 1 - q for q in qargs_A_sorted]
    axes_B = [N - 1 - q for q in qargs_B_sorted]
    
    tensor = data.reshape((2,) * N)
    tensor = np.transpose(tensor, axes_A + axes_B)
    
    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    
    matrix = tensor.reshape((dim_A, dim_B))
    
    U, S, Vh = np.linalg.svd(matrix, full_matrices=False)
    
    results = []
    for i in range(len(S)):
        if S[i] > 1e-12:
            results.append((float(S[i]), U[:, i], Vh[i, :]))
            
    return results
