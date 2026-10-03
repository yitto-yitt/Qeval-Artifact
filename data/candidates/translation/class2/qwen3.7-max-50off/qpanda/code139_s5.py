# EVAL_META: task_id=139, framework=qpanda, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    if hasattr(data, 'data'):
        state = np.array(data.data)
    elif hasattr(data, 'to_matrix'):
        state = np.array(data.to_matrix())
    else:
        state = np.array(data)
        
    is_statevector = (state.ndim == 1)
    N = int(np.round(np.log2(state.shape[0])))
    
    qargs_B = list(qargs_B)
    qargs_A = [i for i in range(N) if i not in qargs_B]
    
    if is_statevector:
        tensor = state.reshape([2] * N)
        tensor = tensor.transpose(tuple(range(N-1, -1, -1)))
        axes_A = tuple(qargs_A)
        axes_B = tuple(qargs_B)
        tensor = tensor.transpose(axes_A + axes_B)
        dim_A = 2 ** len(qargs_A)
        dim_B = 2 ** len(qargs_B)
        mat = tensor.reshape((dim_A, dim_B))
        U, S, Vh = np.linalg.svd(mat, full_matrices=False)
        
        results = []
        for k in range(len(S)):
            if S[k] > 1e-12:
                results.append((float(S[k]), U[:, k], Vh[k, :]))
        return results
    else:
        tensor = state.reshape([2] * (2 * N))
        perm = list(range(N-1, -1, -1)) + list(range(2*N-1, N-1, -1))
        tensor = tensor.transpose(perm)
        
        axes_out_A = tuple(qargs_A)
        axes_in_A = tuple([q + N for q in qargs_A])
        axes_out_B = tuple(qargs_B)
        axes_in_B = tuple([q + N for q in qargs_B])
        
        tensor = tensor.transpose(axes_out_A + axes_in_A + axes_out_B + axes_in_B)
        dim_A = 2 ** len(qargs_A)
        dim_B = 2 ** len(qargs_B)
        mat = tensor.reshape((dim_A * dim_A, dim_B * dim_B))
        U, S, Vh = np.linalg.svd(mat, full_matrices=False)
        
        results = []
        for k in range(len(S)):
            if S[k] > 1e-12:
                results.append((float(S[k]), U[:, k].reshape((dim_A, dim_A)), Vh[k, :].reshape((dim_B, dim_B))))
        return results
