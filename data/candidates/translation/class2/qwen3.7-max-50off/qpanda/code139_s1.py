# EVAL_META: task_id=139, framework=qpanda, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    if hasattr(data, 'data'):
        data = np.array(data.data, dtype=complex)
    else:
        data = np.array(data, dtype=complex)
        
    if data.ndim == 2:
        purity = np.real(np.trace(data @ data))
        if np.abs(purity - 1.0) < 1e-4:
            evals, evecs = np.linalg.eigh(data)
            idx = np.argmax(evals)
            statevec = evecs[:, idx]
            data = statevec
            
    if data.ndim == 1:
        N = int(np.round(np.log2(data.shape[0])))
        qargs_B = sorted(list(qargs_B))
        qargs_A = sorted([q for q in range(N) if q not in qargs_B])
        
        tensor = data.reshape((2,) * N)
        axes_A = [N - 1 - q for q in qargs_A]
        axes_B = [N - 1 - q for q in qargs_B]
        
        tensor = np.transpose(tensor, axes_A + axes_B)
        M = tensor.reshape((2**len(qargs_A), 2**len(qargs_B)))
        
        U, S, Vh = np.linalg.svd(M, full_matrices=False)
        
        result = []
        for k in range(len(S)):
            if S[k] > 1e-12:
                result.append((float(S[k]), U[:, k], Vh[k, :]))
        return result
    elif data.ndim == 2:
        N = int(np.round(np.log2(data.shape[0])))
        qargs_B = sorted(list(qargs_B))
        qargs_A = sorted([q for q in range(N) if q not in qargs_B])
        
        tensor = data.reshape((2,) * (2 * N))
        axes_A_out = [N - 1 - q for q in qargs_A]
        axes_A_in = [2 * N - 1 - q for q in qargs_A]
        axes_B_out = [N - 1 - q for q in qargs_B]
        axes_B_in = [2 * N - 1 - q for q in qargs_B]
        
        tensor = np.transpose(tensor, axes_A_out + axes_A_in + axes_B_out + axes_B_in)
        M = tensor.reshape((2**(2 * len(qargs_A)), 2**(2 * len(qargs_B))))
        
        U, S, Vh = np.linalg.svd(M, full_matrices=False)
        
        result = []
        for k in range(len(S)):
            if S[k] > 1e-12:
                op_A = U[:, k].reshape((2**len(qargs_A), 2**len(qargs_A)))
                op_B = Vh[k, :].reshape((2**len(qargs_B), 2**len(qargs_B)))
                result.append((float(S[k]), op_A, op_B))
        return result
