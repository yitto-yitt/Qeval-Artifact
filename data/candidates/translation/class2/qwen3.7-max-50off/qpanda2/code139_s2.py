# EVAL_META: task_id=139, framework=qpanda2, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    data = np.array(data, dtype=complex)
    if data.ndim == 2:
        evals, evecs = np.linalg.eigh(data)
        psi = evecs[:, np.argmax(evals)]
    else:
        psi = data
        
    n = int(np.round(np.log2(len(psi))))
    qargs_A = sorted([i for i in range(n) if i not in qargs_B])
    
    axes_B = [n - 1 - q for q in qargs_B]
    axes_A = [n - 1 - q for q in qargs_A]
    
    tensor = psi.reshape([2]*n)
    perm = axes_A + axes_B
    tensor = np.transpose(tensor, perm)
    
    dim_A = 2**len(qargs_A)
    dim_B = 2**len(qargs_B)
    mat = tensor.reshape((dim_A, dim_B))
    
    U, S, Vh = np.linalg.svd(mat, full_matrices=False)
    
    result = []
    for i in range(len(S)):
        if S[i] > 1e-12:
            coeff = float(S[i])
            state_A = U[:, i]
            state_B = Vh[i, :]
            result.append((coeff, state_A, state_B))
            
    return result
