# EVAL_META: task_id=139, framework=qpanda, class=2
import numpy as np
from pyqpanda3.core import DensityMatrix

def schmidt_test(data, qargs_B):
    dm = DensityMatrix(data)
    dims = dm.dims()
    if isinstance(dims[0], (list, tuple)):
        n_subsys = len(dims[0])
        dim_list = list(dims[0])
    else:
        n_subsys = int(round(np.log2(np.array(data).shape[0])))
        dim_list = [2] * n_subsys

    qargs_B = list(qargs_B)
    qargs_A = [i for i in range(n_subsys) if i not in qargs_B]
    perm = qargs_A + qargs_B

    arr = np.asarray(data, dtype=complex)
    if arr.ndim == 1:
        vec = arr
    else:
        w, v = np.linalg.eigh(arr)
        idx = int(np.argmax(np.real(w)))
        vec = v[:, idx]

    tensor = vec.reshape(dim_list)
    tensor_perm = np.transpose(tensor, axes=perm)

    dimA = int(np.prod([dim_list[i] for i in qargs_A], dtype=int)) if qargs_A else 1
    dimB = int(np.prod([dim_list[i] for i in qargs_B], dtype=int)) if qargs_B else 1
    mat = tensor_perm.reshape(dimA, dimB)

    U, S, Vh = np.linalg.svd(mat, full_matrices=False)

    terms = []
    for i, s in enumerate(S):
        if np.isclose(s, 0.0):
            continue
        a = U[:, i]
        b = np.conjugate(Vh[i, :])
        terms.append((s, a, b))
    return terms
