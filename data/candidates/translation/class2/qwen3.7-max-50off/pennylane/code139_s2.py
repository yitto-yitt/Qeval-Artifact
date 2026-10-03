# EVAL_META: task_id=139, framework=pennylane, class=2
import numpy as np
import pennylane as qml

def schmidt_test(data, qargs_B):
    data = np.asarray(data)
    if data.ndim == 2 and data.shape[0] == data.shape[1]:
        evals, evecs = np.linalg.eigh(data)
        idx = np.argmax(evals)
        data = evecs[:, idx]
    
    data = data.flatten()
    N = int(np.round(np.log2(len(data))))
    
    qargs_A = [i for i in range(N) if i not in qargs_B]
    
    tensor = data.reshape([2] * N)
    perm = qargs_A + list(qargs_B)
    tensor = np.transpose(tensor, perm)
    
    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    matrix = tensor.reshape(dim_A, dim_B)
    
    U, S, Vh = np.linalg.svd(matrix, full_matrices=False)
    
    result = []
    for i in range(len(S)):
        if S[i] > 1e-12:
            result.append((float(S[i]), U[:, i], Vh[i, :]))
            
    return result
