# EVAL_META: task_id=139, framework=cirq, class=2
import numpy as np
import cirq

def schmidt_test(data, qargs_B):
    # Convert data to numpy array if needed
    if not isinstance(data, np.ndarray):
        if hasattr(data, 'state_vector'):
            data = data.state_vector()
        elif hasattr(data, 'final_state'):
            data = data.final_state
        else:
            data = np.array(data)
    
    # Determine if state vector or density matrix
    if data.ndim == 2:
        # Density matrix
        trace = np.trace(data)
        if not np.isclose(trace, 1.0):
            raise ValueError("Input density matrix must have trace 1.")
        purity = np.trace(np.dot(data, data))
        if not np.isclose(purity, 1.0):
            raise ValueError("Input state must be a pure state.")
        eigvals, eigvecs = np.linalg.eigh(data)
        idx = np.argmax(eigvals)
        state = eigvecs[:, idx]
        state = state / np.linalg.norm(state)
    elif data.ndim == 1:
        state = data
        state = state / np.linalg.norm(state)
    else:
        raise ValueError("Input data must be a state vector or density matrix.")
    
    n = int(np.log2(len(state)))
    if 2**n != len(state):
        raise ValueError("State vector length must be a power of 2.")
    
    B = list(qargs_B)
    if any(b < 0 or b >= n for b in B):
        raise ValueError("Qubit indices out of range.")
    if len(set(B)) != len(B):
        raise ValueError("Duplicate qubit indices in qargs_B.")
    A = [i for i in range(n) if i not in B]
    n_A = len(A)
    n_B = len(B)
    
    # Build permutation of tensor axes
    # Tensor axes: axis i corresponds to qubit n-1-i
    # A qubits in descending order, then B qubits in descending order
    A_sorted_desc = sorted(A, reverse=True)
    B_sorted_desc = sorted(B, reverse=True)
    A_axes = [n - 1 - i for i in A_sorted_desc]
    B_axes = [n - 1 - i for i in B_sorted_desc]
    permutation = A_axes + B_axes
    
    # Reshape state into tensor and permute
    state_tensor = state.reshape([2] * n)
    state_perm = state_tensor.transpose(permutation)
    M = state_perm.reshape(2**n_A, 2**n_B)
    
    # SVD
    U, S, Vh = np.linalg.svd(M, full_matrices=False)
    
    # Build result
    result = []
    for i in range(len(S)):
        coeff = S[i]
        state_A = U[:, i]
        state_B = Vh[i, :].conj()
        result.append((coeff, state_A, state_B))
    
    return result
