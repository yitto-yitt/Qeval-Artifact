# EVAL_META: task_id=139, framework=qpanda2, class=2
import numpy as np
import pyqpanda as pq

try:
    from qiskit.quantum_info import Statevector
    HAS_QISKIT = True
except ImportError:
    HAS_QISKIT = False

def schmidt_test(data, qargs_B):
    if hasattr(data, 'data'):
        vec = np.array(data.data)
    else:
        vec = np.array(data)
    
    n = int(np.log2(len(vec)))
    tensor = vec.reshape([2] * n)
    
    axes_B = [n - 1 - k for k in qargs_B]
    axes_A = [n - 1 - k for k in range(n) if k not in qargs_B]
    
    transposed = np.transpose(tensor, axes_A + axes_B)
    matrix = transposed.reshape(2**len(axes_A), 2**len(axes_B))
    
    U, S, Vt = np.linalg.svd(matrix, full_matrices=False)
    
    results = []
    for i in range(len(S)):
        coeff = S[i]
        state_A = U[:, i]
        state_B = Vt[i, :]
        if HAS_QISKIT:
            results.append((coeff, Statevector(state_A), Statevector(state_B)))
        else:
            results.append((coeff, state_A, state_B))
            
    return results
