# EVAL_META: task_id=139, framework=cirq, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    data = np.asarray(data)
    if data.ndim == 2:
        evals, evecs = np.linalg.eigh(data)
        idx = np.argmax(evals)
        state = evecs[:, idx]
    else:
        state = data
        
    n = int(np.round(np.log2(state.shape[0])))
    
    if isinstance(qargs_B, int):
        qargs_B = [qargs_B]
        
    qargs_A = sorted([q for q in range(n) if q not in qargs_B])
    qargs_B_sorted = sorted(qargs_B)
    
    axes_A = [n - 1 - q for q in qargs_A]
    axes_B = [n - 1 - q for q in qargs_B_sorted]
    
    tensor = state.reshape((2,) * n)
    tensor = tensor.transpose(axes_A + axes_B)
    mat = tensor.reshape((2**len(qargs_A), 2**len(qargs_B)))
    
    U, S, Vh = np.linalg.svd(mat, full_matrices=False)
    
    terms = []
    for i in range(len(S)):
        if S[i] > 1e-12:
            terms.append((float(S[i]), U[:, i], Vh[i, :]))
            
    return terms
