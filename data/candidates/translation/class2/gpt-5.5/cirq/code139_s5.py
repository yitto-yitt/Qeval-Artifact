# EVAL_META: task_id=139, framework=cirq, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    dims = None
    if hasattr(data, "dims") and callable(getattr(data, "dims")):
        try:
            raw_dims = data.dims()
            if raw_dims and isinstance(raw_dims[0], (tuple, list)):
                raw_dims = raw_dims[0]
            dims = [int(d) for d in raw_dims]
        except Exception:
            dims = None

    if not isinstance(data, (list, tuple, np.ndarray)) and hasattr(data, "data"):
        arr = np.asarray(data.data, dtype=complex)
    else:
        arr = np.asarray(data, dtype=complex)

    if arr.ndim == 2 and 1 in arr.shape:
        vec = arr.reshape(-1)
    elif arr.ndim == 2 and arr.shape[0] == arr.shape[1]:
        vals, vecs = np.linalg.eigh(arr)
        idx = int(np.argmax(vals.real))
        scale = np.sqrt(max(float(vals[idx].real), 0.0))
        vec = vecs[:, idx] * scale
    else:
        vec = arr.reshape(-1)

    total_dim = int(vec.size)

    if dims is None or int(np.prod(dims, dtype=int)) != total_dim:
        n_float = np.log2(total_dim)
        n = int(round(n_float))
        if 2 ** n != total_dim:
            raise ValueError("Input state dimension is not a power of 2 and no valid subsystem dimensions were provided.")
        dims = [2] * n
    else:
        n = len(dims)

    if qargs_B is None:
        qargs_B = []
    elif isinstance(qargs_B, (int, np.integer)):
        qargs_B = [int(qargs_B)]
    else:
        qargs_B = [int(q) for q in qargs_B]

    if len(set(qargs_B)) != len(qargs_B):
        raise ValueError("Duplicate subsystem arguments are not allowed.")
    if any(q < 0 or q >= n for q in qargs_B):
        raise ValueError("Subsystem argument is out of range.")

    qargs_A = [q for q in range(n) if q not in set(qargs_B)]

    dim_A = int(np.prod([dims[q] for q in qargs_A], dtype=int)) if qargs_A else 1
    dim_B = int(np.prod([dims[q] for q in qargs_B], dtype=int)) if qargs_B else 1

    tensor_shape = [dims[q] for q in range(n - 1, -1, -1)]
    tensor = np.reshape(vec, tensor_shape)

    axes = [n - 1 - q for q in reversed(qargs_A)] + [n - 1 - q for q in reversed(qargs_B)]
    matrix = np.transpose(tensor, axes).reshape((dim_A, dim_B))

    u, s, vh = np.linalg.svd(matrix, full_matrices=False)

    return [(s[i], np.array(u[:, i], dtype=complex), np.array(vh[i, :], dtype=complex))
            for i in range(len(s)) if not np.isclose(s[i], 0)]
