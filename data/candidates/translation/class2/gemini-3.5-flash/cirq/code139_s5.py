# EVAL_META: task_id=139, framework=cirq, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    # Convert data to numpy array
    state = np.asarray(data, dtype=np.complex128)
    N = int(np.round(np.log2(state.size)))
    
    # Reshape to N-dimensional tensor
    tensor = state.reshape([2] * N)
    
    # Identify axes for A and B
    qargs_B_indices = []
    for q in qargs_B:
        if isinstance(q, int):
            qargs_B_indices.append(q)
        elif hasattr(q, 'x'):
            qargs_B_indices.append(int(q.x))
        else:
            try:
                qargs_B_indices.append(int(q))
            except:
                pass

    axes_B = list(qargs_B_indices)
    axes_A = [i for i in range(N) if i not in axes_B]
    
    # Transpose tensor to group A axes first, then B axes
    perm = axes_A + axes_B
    tensor_transposed = np.transpose(tensor, perm)
    
    # Reshape to 2D matrix of shape (2**len(A), 2**len(B))
    dim_A = 2 ** len(axes_A)
    dim_B = 2 ** len(axes_B)
    matrix = tensor_transposed.reshape((dim_A, dim_B))
    
    # Perform SVD
    U, S, Vt = np.linalg.svd(matrix)
    
    # Filter out zero singular values with a tolerance
    tolerance = 1e-9
    
    terms = []
    for i in range(len(S)):
        if S[i] > tolerance:
            coeff = float(S[i])
            state_A = U[:, i]
            state_B = Vt[i, :]
            terms.append((coeff, state_A, state_B))
            
    return terms
