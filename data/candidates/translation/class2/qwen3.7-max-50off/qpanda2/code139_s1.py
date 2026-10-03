# EVAL_META: task_id=139, framework=qpanda2, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    data = np.asarray(data, dtype=complex)
    if isinstance(qargs_B, int):
        qargs_B = [qargs_B]
        
    if data.ndim == 1:
        N = int(np.round(np.log2(data.shape[0])))
        qargs_A = [i for i in range(N) if i not in qargs_B]
        tensor = data.reshape((2,) * N)
        perm = [N - 1 - i for i in qargs_A] + [N - 1 - i for i in qargs_B]
        tensor = np.transpose(tensor, perm)
        dim_A = 2 ** len(qargs_A)
        dim_B = 2 ** len(qargs_B)
        mat = tensor.reshape((dim_A, dim_B))
        U, S, Vh = np.linalg.svd(mat, full_matrices=False)
        res = []
        for i in range(len(S)):
            if S[i] > 1e-15:
                res.append((float(S[i]), U[:, i], Vh[i, :]))
        return res
    elif data.ndim == 2:
        N = int(np.round(np.log2(data.shape[0])))
        qargs_A = [i for i in range(N) if i not in qargs_B]
        tensor = data.reshape((2,) * (2 * N))
        perm_A = [N - 1 - i for i in qargs_A] + [2 * N - 1 - i for i in qargs_A]
        perm_B = [N - 1 - i for i in qargs_B] + [2 * N - 1 - i for i in qargs_B]
        perm = perm_A + perm_B
        tensor = np.transpose(tensor, perm)
        dim_A = 2 ** (2 * len(qargs_A))
        dim_B = 2 ** (2 * len(qargs_B))
        mat = tensor.reshape((dim_A, dim_B))
        U, S, Vh = np.linalg.svd(mat, full_matrices=False)
        res = []
        for i in range(len(S)):
            if S[i] > 1e-15:
                res.append((float(S[i]), U[:, i], Vh[i, :]))
        return res
    else:
        raise ValueError("Unsupported data dimensions")
