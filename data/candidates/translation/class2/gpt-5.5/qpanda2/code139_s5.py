# EVAL_META: task_id=139, framework=qpanda2, class=2
import numpy as np
import pyqpanda as pq

def schmidt_test(data, qargs_B):
    if hasattr(data, "data"):
        vec = np.asarray(data.data, dtype=complex)
    else:
        vec = np.asarray(data, dtype=complex)

    if vec.ndim == 2 and 1 in vec.shape:
        vec = vec.reshape(-1)
    elif vec.ndim != 1:
        vals, vecs = np.linalg.eigh(vec)
        vec = vecs[:, int(np.argmax(vals))]

    dim = vec.size

    dims = None
    if hasattr(data, "dims"):
        try:
            dims_val = data.dims()
            if isinstance(dims_val, tuple):
                dims = tuple(int(x) for x in dims_val)
        except Exception:
            dims = None

    if dims is None:
        n = int(round(np.log2(dim))) if dim > 0 else 0
        if 2 ** n == dim:
            dims = (2,) * n
        else:
            dims = (dim,)

    num_subsystems = len(dims)
    qargs_B = sorted([int(q) for q in qargs_B])
    qargs_A = [q for q in range(num_subsystems) if q not in qargs_B]

    dims_A = tuple(dims[q] for q in qargs_A)
    dims_B = tuple(dims[q] for q in qargs_B)

    dim_A = int(np.prod(dims_A, dtype=int)) if dims_A else 1
    dim_B = int(np.prod(dims_B, dtype=int)) if dims_B else 1

    tensor = vec.reshape(dims, order="F")
    axes = qargs_A + qargs_B
    if axes:
        tensor = np.transpose(tensor, axes)

    mat = tensor.reshape((dim_A, dim_B), order="F")
    u, s, vh = np.linalg.svd(mat, full_matrices=False)

    tol = max(mat.shape) * np.finfo(float).eps * (s[0] if s.size else 0.0)
    terms = []
    for i, coeff in enumerate(s):
        if coeff > tol:
            terms.append((coeff, np.array(u[:, i], dtype=complex), np.array(vh[i, :], dtype=complex)))
    return terms
