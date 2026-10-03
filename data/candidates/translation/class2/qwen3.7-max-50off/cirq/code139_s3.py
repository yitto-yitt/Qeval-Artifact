# EVAL_META: task_id=139, framework=cirq, class=2
import numpy as np
import cirq

def schmidt_test(data, qargs_B):
    data = np.array(data, dtype=complex)
    if data.ndim == 2:
        evals, evecs = np.linalg.eigh(data)
        idx = np.argmax(evals)
        data = evecs[:, idx]
        
    n_qubits = int(np.round(np.log2(data.shape[0])))
    
    if isinstance(qargs_B, int):
        qargs_B = [qargs_B]
        
    qargs_A = [i for i in range(n_qubits) if i not in qargs_B]
    
    shape = [2] * n_qubits
    tensor = data.reshape(shape)
    
    axes_A = [n_qubits - 1 - q for q in sorted(qargs_A, reverse=True)]
    axes_B = [n_qubits - 1 - q for q in sorted(qargs_B, reverse=True)]
    
    tensor = np.transpose(tensor, axes=axes_A + axes_B)
    
    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    
    matrix = tensor.reshape((dim_A, dim_B))
    
    U, S, Vh = np.linalg.svd(matrix, full_matrices=False)
    
    result = []
    for i in range(len(S)):
        if S[i] > 1e-10:
            coeff = float(S[i])
            state_A = U[:, i]
            state_B = Vh[i, :]
            result.append((coeff, state_A, state_B))
            
    return result
