# EVAL_META: task_id=139, framework=cirq, class=2
import numpy as np
import cirq

def schmidt_test(data, qargs_B):
    # Convert data to state vector
    state = np.asarray(data)
    if state.ndim == 2:
        evals, evecs = np.linalg.eigh(state)
        state = evecs[:, -1]
    
    n_qubits = int(np.round(np.log2(len(state))))
    
    # Helper to convert qubit to index
    def to_index(q):
        if isinstance(q, int):
            return q
        if hasattr(q, 'x'):
            return q.x
        import re
        match = re.search(r'\d+', str(q))
        if match:
            return int(match.group())
        return 0

    qargs_B_indices = [to_index(q) for q in qargs_B]
    
    # In Cirq, qubit i corresponds to axis i
    axes_B = qargs_B_indices
    axes_A = [i for i in range(n_qubits) if i not in axes_B]
    
    # Reshape to tensor of shape (2, 2, ..., 2)
    tensor = np.reshape(state, [2] * n_qubits)
    
    # Permute axes so A comes first, then B
    perm = axes_A + axes_B
    tensor_perm = np.transpose(tensor, perm)
    
    # Reshape to (2**n_A, 2**n_B)
    n_A = len(axes_A)
    n_B = len(axes_B)
    matrix = np.reshape(tensor_perm, (2**n_A, 2**n_B))
    
    # SVD
    U, S, Vh = np.linalg.svd(matrix, full_matrices=False)
    
    results = []
    for i in range(len(S)):
        coeff = S[i]
        state_A = U[:, i]
        state_B = Vh[i, :]
        results.append((coeff, state_A, state_B))
        
    return results
