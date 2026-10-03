# EVAL_META: task_id=139, framework=pennylane, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    """
    Compute the Schmidt decomposition of a pure state given by a density matrix.
    
    Args:
        data: 2D numpy array representing a density matrix.
        qargs_B: list of qubit indices for subsystem B.
    
    Returns:
        List of tuples (coeff, state_A, state_B) where coeff is the Schmidt coefficient,
        state_A is a 1D complex array for subsystem A, and state_B is a 1D complex array for subsystem B.
    """
    # determine total number of qubits
    n = int(np.log2(data.shape[0]))
    
    # find the pure statevector from the density matrix
    eigvals, eigvecs = np.linalg.eigh(data)
    # eigenvector with the largest eigenvalue (should be close to 1 for pure state)
    idx = np.argmax(eigvals)
    state = eigvecs[:, idx]
    
    # reshape to [2]*n
    state_reshaped = state.reshape([2] * n)
    
    # partition: A qubits are all indices not in qargs_B
    A_indices = [i for i in range(n) if i not in qargs_B]
    # permutation: sorted A first, then B as given
    perm = sorted(A_indices) + list(qargs_B)
    state_perm = np.transpose(state_reshaped, axes=perm)
    
    dimA = 2 ** len(A_indices)
    dimB = 2 ** len(qargs_B)
    mat = state_perm.reshape((dimA, dimB))
    
    # singular value decomposition
    U, S, Vh = np.linalg.svd(mat, full_matrices=False)
    
    # construct result
    result = []
    for k in range(len(S)):
        coeff = S[k]
        state_A = U[:, k]
        state_B = Vh[k, :]
        result.append((coeff, state_A, state_B))
    
    return result
