# EVAL_META: task_id=139, framework=qpanda2, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    data = np.array(data, dtype=complex)
    if data.ndim == 2:
        w, v = np.linalg.eigh(data)
        idx = np.argmax(w)
        data = v[:, idx]
        
    N = int(np.round(np.log2(len(data))))
    tensor = data.reshape((2,) * N)
    qargs_A = [i for i in range(N) if i not in qargs_B]
    axes_A = [N - 1 - j for j in qargs_A]
    axes_B = [N - 1 - j for j in qargs_B]
    mat = tensor.transpose(axes_A + axes_B).reshape(2**len(qargs_A), 2**len(qargs_B))
    U, S, Vh = np.linalg.svd(mat, full_matrices=False)
    res = []
    for i in range(len(S)):
        if S[i] > 1e-10:
            res.append((float(S[i]), U[:, i], Vh[i, :]))
    return res
