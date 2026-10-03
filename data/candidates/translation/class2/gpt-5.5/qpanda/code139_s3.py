# EVAL_META: task_id=139, framework=qpanda, class=2
from pyqpanda3.core import *
import numpy as np

def schmidt_test(data, qargs_B):
    obj = data

    dims = None
    if hasattr(obj, "dims") and callable(getattr(obj, "dims")):
        try:
            dims = tuple(int(x) for x in obj.dims())
        except Exception:
            dims = None

    arr = np.asarray(getattr(obj, "data", obj), dtype=complex)

    if arr.ndim == 2 and arr.shape[0] == arr.shape[1]:
        if dims is None:
            dim = arr.shape[0]
            if dim > 0 and (dim & (dim - 1)) == 0:
                dims = (2,) * int(np.log2(dim))
            else:
                dims = (dim,)
        vals, vecs = np.linalg.eigh(arr)
        idx = int(np.argmax(np.real(vals)))
        vec = vecs[:, idx] * np.sqrt(max(float(np.real(vals[idx])), 0.0))
        arr = vec
    else:
        arr = arr.reshape(-1)

    if dims is None:
        dim = int(arr.size)
        if dim > 0 and (dim & (dim - 1)) == 0:
            dims = (2,) * int(np.log2(dim))
        else:
            dims = (dim,)

    nsub = len(dims)
    if qargs_B is None:
        qargs_B = [0]
    qargs_B = sorted(int(q) for q in qargs_B)
    qargs_A = [q for q in range(nsub) if q not in qargs_B]

    tensor = arr.reshape(tuple(reversed(dims)))
    axes = [nsub - 1 - q for q in reversed(qargs_A)] + [nsub - 1 - q for q in reversed(qargs_B)]
    tensor = np.transpose(tensor, axes) if axes else tensor

    dim_A = int(np.prod([dims[q] for q in qargs_A], dtype=int)) if qargs_A else 1
    dim_B = int(np.prod([dims[q] for q in qargs_B], dtype=int)) if qargs_B else 1
    mat = tensor.reshape((dim_A, dim_B))

    u, s, vh = np.linalg.svd(mat, full_matrices=False)

    terms = []
    for i, coeff in enumerate(s):
        if coeff > 1e-10:
            terms.append((float(coeff), np.array(u[:, i], dtype=complex), np.array(vh[i, :], dtype=complex)))
    return terms
