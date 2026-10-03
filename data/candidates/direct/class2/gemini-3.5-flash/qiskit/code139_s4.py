# EVAL_META: task_id=139, framework=qiskit, class=2

import numpy as np
from qiskit.quantum_info import DensityMatrix, Statevector

def schmidt_test(data, qargs_B):
    if isinstance(data, DensityMatrix):
        eigvals, eigvecs = np.linalg.eigh(data.data)
        psi = eigvecs[:, -1]
    elif isinstance(data, Statevector):
        psi = data.data
    else:
        arr = np.array(data)
        if arr.ndim == 2:
            eigvals, eigvecs = np.linalg.eigh(arr)
            psi = eigvecs[:, -1]
        else:
            psi = arr
            
    n = int(np.round(np.log2(len(psi))))
    
    qargs_B = list(qargs_B)
    qargs_A = [i for i in range(n) if i not in qargs_B]
    
    qargs_A.sort()
    qargs_B.sort()
    
    axis_map = {k: n - 1 - k for k in range(n)}
    axes_A = [axis_map[k] for k in qargs_A]
    axes_B = [axis_map[k] for k in qargs_B]
    
    permuted_axes = axes_A + axes_B
    tensor = psi.reshape([2] * n)
    permuted_tensor = np.transpose(tensor, permuted_axes)
    
    matrix = permuted_tensor.reshape((2**len(qargs_A), 2**len(qargs_B)))
    
    U, S, Vt = np.linalg.svd(matrix, full_matrices=False)
    
    results = []
    for i in range(len(S)):
        coeff = S[i]
        state_A = U[:, i]
        state_B = Vt[i, :]
        results.append((coeff, state_A, state_B))
        
    return results
