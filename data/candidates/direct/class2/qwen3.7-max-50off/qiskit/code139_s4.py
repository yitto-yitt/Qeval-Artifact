# EVAL_META: task_id=139, framework=qiskit, class=2
import numpy as np
from qiskit.quantum_info import Statevector, DensityMatrix

def schmidt_test(data, qargs_B):
    if isinstance(data, DensityMatrix):
        evals, evecs = np.linalg.eigh(data.data)
        idx = np.argmax(evals)
        psi = evecs[:, idx]
    elif isinstance(data, Statevector):
        psi = data.data
    else:
        arr = np.asarray(data)
        if arr.ndim == 1:
            psi = arr
        else:
            evals, evecs = np.linalg.eigh(arr)
            idx = np.argmax(evals)
            psi = evecs[:, idx]
            
    N = int(np.round(np.log2(len(psi))))
    qargs_A = [i for i in range(N) if i not in qargs_B]
    
    axes_A = [N - 1 - q for q in qargs_A]
    axes_B = [N - 1 - q for q in qargs_B]
    
    psi_tensor = psi.reshape([2]*N)
    psi_tensor = np.transpose(psi_tensor, axes_A + axes_B)
    
    dim_A = 2**len(qargs_A)
    dim_B = 2**len(qargs_B)
    M = psi_tensor.reshape((dim_A, dim_B))
    
    U, S, Vh = np.linalg.svd(M, full_matrices=False)
    
    idx_sort = np.argsort(S)[::-1]
    S = S[idx_sort]
    U = U[:, idx_sort]
    Vh = Vh[idx_sort, :]
    
    terms = []
    for i in range(len(S)):
        if S[i] > 1e-12:
            c = float(S[i])
            a = U[:, i]
            b = Vh[i, :]
            terms.append((c, a, b))
            
    return terms
