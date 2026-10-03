# EVAL_META: task_id=139, framework=qiskit, class=2

import numpy as np
from qiskit.quantum_info import Statevector, DensityMatrix

def schmidt_test(data, qargs_B):
    if isinstance(data, DensityMatrix):
        evals, evecs = np.linalg.eigh(data.data)
        psi = evecs[:, np.argmax(evals)]
    elif isinstance(data, Statevector):
        psi = data.data
    else:
        arr = np.array(data)
        if arr.ndim == 2 and arr.shape[0] == arr.shape[1]:
            evals, evecs = np.linalg.eigh(arr)
            psi = evecs[:, np.argmax(evals)]
        else:
            psi = arr

    n = int(np.log2(len(psi)))
    
    qargs_B = sorted(list(qargs_B))
    qargs_A = sorted([q for q in range(n) if q not in qargs_B])
    
    axes_A = [n - 1 - q for q in reversed(qargs_A)]
    axes_B = [n - 1 - q for q in reversed(qargs_B)]
    
    tensor = psi.reshape([2] * n)
    perm = axes_A + axes_B
    transposed = np.transpose(tensor, perm)
    
    matrix = transposed.reshape((2**len(qargs_A), 2**len(qargs_B)))
    
    U, S, Vh = np.linalg.svd(matrix, full_matrices=False)
    
    terms = []
    for i in range(len(S)):
        coeff = S[i]
        state_A = Statevector(U[:, i])
        state_B = Statevector(Vh[i, :])
        terms.append((coeff, state_A, state_B))
        
    return terms
