# EVAL_META: task_id=139, framework=qpanda, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    if isinstance(qargs_B, int):
        qargs_B = [qargs_B]
        
    state = np.array(data, dtype=complex)
    if state.ndim == 1:
        n = int(np.round(np.log2(state.shape[0])))
        qargs_A = [i for i in range(n) if i not in qargs_B]
        
        dims = [2] * n
        tensor = state.reshape(dims)
        
        axes_A = [n - 1 - j for j in qargs_A]
        axes_B = [n - 1 - j for j in qargs_B]
        
        tensor = np.transpose(tensor, axes_A + axes_B)
        
        dim_A = 2 ** len(qargs_A)
        dim_B = 2 ** len(qargs_B)
        mat = tensor.reshape(dim_A, dim_B)
        
        U, S, Vh = np.linalg.svd(mat, full_matrices=False)
        
        terms = []
        for i in range(len(S)):
            if S[i] > 1e-10:
                sA = U[:, i]
                sB = Vh[i, :]
                terms.append((float(S[i]), sA, sB))
        return terms
        
    elif state.ndim == 2:
        n = int(np.round(np.log2(state.shape[0])))
        qargs_A = [i for i in range(n) if i not in qargs_B]
        
        dims = [2] * (2 * n)
        tensor = state.reshape(dims)
        
        axes_A_row = [n - 1 - j for j in qargs_A]
        axes_B_row = [n - 1 - j for j in qargs_B]
        axes_A_col = [2 * n - 1 - j for j in qargs_A]
        axes_B_col = [2 * n - 1 - j for j in qargs_B]
        
        tensor = np.transpose(tensor, axes_A_row + axes_A_col + axes_B_row + axes_B_col)
        
        dim_A = 2 ** (2 * len(qargs_A))
        dim_B = 2 ** (2 * len(qargs_B))
        mat = tensor.reshape(dim_A, dim_B)
        
        U, S, Vh = np.linalg.svd(mat, full_matrices=False)
        
        terms = []
        for i in range(len(S)):
            if S[i] > 1e-10:
                sA = U[:, i].reshape(2**len(qargs_A), 2**len(qargs_A))
                sB = Vh[i, :].reshape(2**len(qargs_B), 2**len(qargs_B))
                terms.append((float(S[i]), sA, sB))
        return terms
