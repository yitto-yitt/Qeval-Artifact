# EVAL_META: task_id=139, framework=pennylane, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    # Convert input to numpy array
    state = np.array(data)
    
    # Normalize qargs_B to a list
    if isinstance(qargs_B, int):
        qargs_B = [qargs_B]
    else:
        qargs_B = list(qargs_B)
    
    # Determine if state is a statevector or density matrix
    if state.ndim == 1:
        num_qubits = int(np.log2(len(state)))
        statevec = state
    elif state.ndim == 2:
        # Density matrix: extract statevector if pure
        eigvals, eigvecs = np.linalg.eigh(state)
        idx = np.argmax(eigvals)
        if not np.isclose(eigvals[idx], 1.0, atol=1e-8):
            raise ValueError("Density matrix is not a pure state.")
        statevec = eigvecs[:, idx]
        num_qubits = int(np.log2(state.shape[0]))
    else:
        raise ValueError("Input must be a statevector or density matrix.")
    
    # Compute qargs_A as the complement of qargs_B
    qargs_A = [i for i in range(num_qubits) if i not in qargs_B]
    
    # Reshape statevector into tensor and permute axes
    state_tensor = statevec.reshape([2] * num_qubits)
    perm = qargs_A + qargs_B
    state_perm = np.transpose(state_tensor, axes=perm)
    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    M = state_perm.reshape((dim_A, dim_B))
    
    # Perform SVD
    U, S, Vh = np.linalg.svd(M, full_matrices=False)
    
    # Filter by cutoff and build result
    cutoff = 1e-16
    terms = []
    for i in range(len(S)):
        if S[i] > cutoff:
            terms.append((S[i], U[:, i], Vh[i, :].conj()))
    return terms
```
