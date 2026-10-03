# EVAL_META: task_id=139, framework=pennylane, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    state = np.asarray(data)
    if hasattr(data, 'dims'):
        dims = data.dims()
    else:
        size = state.size
        ndim = int(np.round(np.log2(size)))
        dims = [2] * ndim
    
    if isinstance(qargs_B, int):
        qargs_B = [qargs_B]
    else:
        qargs_B = list(qargs_B)
        
    qargs_A = [i for i in range(len(dims)) if i not in qargs_B]
    
    dims_A = [dims[i] for i in qargs_A]
    dims_B = [dims[i] for i in qargs_B]
    
    ndim = len(dims)
    tensor = np.reshape(state, dims[::-1])
    
    axes_A = [ndim - 1 - i for i in qargs_A]
    axes_B = [ndim - 1 - i for i in qargs_B]
    
    tensor = np.transpose(tensor, axes_A + axes_B)
    matrix = np.reshape(tensor, (np.prod(dims_A), np.prod(dims_B)))
    
    U, s, Vh = np.linalg.svd(matrix, full_matrices=False)
    
    return [(s[i], U[:, i], Vh[i, :]) for i in range(len(s))]
