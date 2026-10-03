# EVAL_META: task_id=139, framework=qpanda, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    if hasattr(data, 'data'):
        data = np.array(data.data)
    elif hasattr(data, 'to_matrix'):
        data = np.array(data.to_matrix())
    else:
        data = np.array(data)
        
    if isinstance(qargs_B, int):
        qargs_B = [qargs_B]
        
    if data.ndim == 2:
        evals, evecs = np.linalg.eigh(data)
        idx = np.argmax(evals)
        psi = evecs[:, idx]
    elif data.ndim == 1:
        psi = data
    else:
        raise ValueError("Invalid data format")
        
    n_qubits = int(np.round(np.log2(len(psi))))
    qargs_A = [i for i in range(n_qubits) if i not in qargs_B]
    
    axes_B = [n_qubits - 1 - q for q in qargs_B]
    axes_A = [n_qubits - 1 - q for q in qargs_A]
    
    psi_tensor = psi.reshape([2] * n_qubits)
    psi_tensor = np.transpose(psi_tensor, axes_A + axes_B)
    
    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    M = psi_tensor.reshape((dim_A, dim_B))
    
    U, S, Vh = np.linalg.svd(M)
    
    terms = []
    for i in range(len(S)):
        if S[i] > 1e-10:
            coeff = float(S[i])
            state_A = U[:, i]
            state_B = Vh[i, :]
            terms.append((coeff, state_A, state_B))
            
    return terms
