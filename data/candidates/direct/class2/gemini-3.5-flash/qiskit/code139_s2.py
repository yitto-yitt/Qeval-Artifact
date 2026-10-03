# EVAL_META: task_id=139, framework=qiskit, class=2

import numpy as np
from qiskit.quantum_info import DensityMatrix, Statevector

def schmidt_test(data, qargs_B):
    if isinstance(data, DensityMatrix):
        evals, evecs = np.linalg.eigh(data.data)
        idx = np.argmax(evals)
        psi = evecs[:, idx]
        num_qubits = data.num_qubits
    elif isinstance(data, Statevector):
        psi = data.data
        num_qubits = data.num_qubits
    else:
        arr = np.asarray(data)
        if arr.ndim == 2:
            evals, evecs = np.linalg.eigh(arr)
            idx = np.argmax(evals)
            psi = evecs[:, idx]
            num_qubits = int(np.log2(arr.shape[0]))
        else:
            psi = arr
            num_qubits = int(np.log2(arr.shape[0]))
            
    n = num_qubits
    qargs_A = [i for i in range(n) if i not in qargs_B]
    
    qargs_A_desc = sorted(qargs_A, reverse=True)
    qargs_B_desc = sorted(qargs_B, reverse=True)
    
    axes_A = [n - 1 - q for q in qargs_A_desc]
    axes_B = [n - 1 - q for q in qargs_B_desc]
    
    tensor = psi.reshape([2] * n)
    permuted_tensor = np.transpose(tensor, axes_A + axes_B)
    
    size_A = 2 ** len(qargs_A)
    size_B = 2 ** len(qargs_B)
    matrix = permuted_tensor.reshape((size_A, size_B))
    
    U, S, Vh = np.linalg.svd(matrix)
    
    results = []
    for i in range(len(S)):
        coeff = S[i]
        state_A = Statevector(U[:, i])
        state_B = Statevector(Vh[i, :])
        results.append((coeff, state_A, state_B))
        
    return results
