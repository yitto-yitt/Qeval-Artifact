# EVAL_META: task_id=139, framework=qpanda2, class=2
import numpy as np
import pyqpanda as pq

def schmidt_test(data, qargs_B):
    state = np.asarray(data, dtype=complex)
    if state.ndim == 2:
        eigvals, eigvecs = np.linalg.eigh(state)
        state = eigvecs[:, np.argmax(eigvals)]
        
    N = int(round(np.log2(len(state))))
    qargs_B = list(qargs_B)
    qargs_A = [i for i in range(N) if i not in qargs_B]
    
    pattern = qargs_B + qargs_A
    
    axis_perm = [0] * N
    for i in range(N):
        axis_perm[N - 1 - i] = N - 1 - pattern[i]
        
    tensor = state.reshape([2] * N)
    permuted = np.transpose(tensor, axis_perm)
    
    n_B = len(qargs_B)
    n_A = len(qargs_A)
    
    matrix = permuted.reshape((2**n_A, 2**n_B))
    
    U, S, Vt = np.linalg.svd(matrix, full_matrices=False)
    
    results = []
    for i in range(len(S)):
        coeff = S[i]
        state_A = U[:, i]
        state_B = Vt[i, :]
        results.append((coeff, state_A, state_B))
        
    return results
