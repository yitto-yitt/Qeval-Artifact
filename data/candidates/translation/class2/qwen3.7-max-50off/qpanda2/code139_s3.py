# EVAL_META: task_id=139, framework=qpanda2, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    state = np.asarray(data, dtype=complex)
    if state.ndim == 2 and state.shape[0] == state.shape[1] and state.shape[0] > 1:
        eigvals, eigvecs = np.linalg.eigh(state)
        idx = np.argmax(eigvals)
        state = eigvecs[:, idx]
    state = state.flatten()
    
    n = int(np.round(np.log2(len(state))))
    
    qargs_A = [i for i in range(n) if i not in qargs_B]
    axes_A = [n - 1 - i for i in sorted(qargs_A, reverse=True)]
    axes_B = [n - 1 - i for i in sorted(qargs_B, reverse=True)]
    
    tensor = state.reshape([2] * n)
    tensor = np.transpose(tensor, axes_A + axes_B)
    
    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    mat = tensor.reshape((dim_A, dim_B))
    
    u, s, vh = np.linalg.svd(mat, full_matrices=False)
    
    terms = []
    for i in range(len(s)):
        if s[i] > 1e-10:
            terms.append((float(s[i]), u[:, i], vh[i, :]))
            
    return terms
