# EVAL_META: task_id=139, framework=cirq, class=2
import numpy as np
import cirq

def schmidt_test(data, qargs_B):
    if isinstance(data, cirq.StateVector):
        arr = data.state_vector()
    elif isinstance(data, cirq.DensityMatrix):
        arr = data.density_matrix()
    else:
        arr = np.asarray(data)
    
    if arr.ndim == 2:
        vals, vecs = np.linalg.eigh(arr)
        idx = np.argsort(vals)[::-1]
        vals = vals[idx]
        vecs = vecs[:, idx]
        if not np.isclose(vals[0], 1.0) or not np.allclose(vals[1:], 0.0):
            raise ValueError("Input density matrix is not a pure state.")
        state_vec = vecs[:, 0]
    elif arr.ndim == 1:
        state_vec = arr
    else:
        raise ValueError("Input must be a state vector or density matrix.")
    
    norm = np.linalg.norm(state_vec)
    if norm > 0:
        state_vec = state_vec / norm
    else:
        raise ValueError("State vector has zero norm.")
    
    num_qubits = int(np.round(np.log2(len(state_vec))))
    if 2**num_qubits != len(state_vec):
        raise ValueError("State vector length is not a power of 2.")
    
    dims = [2] * num_qubits
    
    if isinstance(qargs_B, int):
        qargs_B = [qargs_B]
    else:
        qargs_B = list(qargs_B)
    
    qargs_A = [i for i in range(num_qubits) if i not in qargs_B]
    
    state_tensor = state_vec.reshape(dims)
    perm = qargs_A + qargs_B
    state_tensor = np.transpose(state_tensor, perm)
    
    dim_A = int(np.prod([dims[i] for i in qargs_A]))
    dim_B = int(np.prod([dims[i] for i in qargs_B]))
    mat = state_tensor.reshape(dim_A, dim_B)
    
    U, S, Vh = np.linalg.svd(mat, full_matrices=False)
    
    result = []
    cutoff = 1e-15
    for i in range(len(S)):
        coeff = float(S[i])
        if coeff > cutoff:
            state_A = U[:, i]
            state_B = Vh[i, :].conj()
            result.append((coeff, state_A, state_B))
    return result
