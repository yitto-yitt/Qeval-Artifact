# EVAL_META: task_id=139, framework=qpanda, class=2
import numpy as np
import pyqpanda3.core as pq

def schmidt_test(data, qargs_B):
    psi = np.asarray(data)
    if psi.ndim == 2:
        eigvals, eigvecs = np.linalg.eigh(psi)
        psi = eigvecs[:, -1]
    
    num_qubits = int(np.log2(len(psi)))
    
    qargs_B = list(qargs_B)
    qargs_A = [i for i in range(num_qubits) if i not in qargs_B]
    
    qargs_A_sorted = sorted(qargs_A, reverse=True)
    qargs_B_sorted = sorted(qargs_B, reverse=True)
    
    axes_A = [num_qubits - 1 - i for i in qargs_A_sorted]
    axes_B = [num_qubits - 1 - i for i in qargs_B_sorted]
    
    tensor = psi.reshape([2] * num_qubits)
    transposed = np.transpose(tensor, axes_A + axes_B)
    matrix = transposed.reshape(2**len(qargs_A), 2**len(qargs_B))
    
    u, s, vh = np.linalg.svd(matrix, full_matrices=False)
    
    tol = 1e-9
    results = []
    for i in range(len(s)):
        if s[i] > tol:
            results.append((s[i], u[:, i], vh[i, :]))
            
    return results
