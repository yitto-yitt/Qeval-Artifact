# EVAL_META: task_id=139, framework=qpanda, class=2
import numpy as np
import pyqpanda3.core as pq

def schmidt_test(data, qargs_B):
    _ = pq

    dims = None
    if hasattr(data, "dims") and callable(getattr(data, "dims")):
        try:
            dims = tuple(int(x) for x in data.dims())
        except Exception:
            dims = None

    arr = np.asarray(getattr(data, "data", data), dtype=complex)

    if arr.ndim == 2:
        if 1 in arr.shape:
            arr = arr.reshape(-1)
        elif arr.shape[0] == arr.shape[1]:
            diag = np.diag(arr)
            idx = int(np.argmax(np.abs(diag)))
            if np.isclose(diag[idx], 0.0):
                arr = np.zeros(arr.shape[0], dtype=complex)
            else:
                arr = arr[:, idx] / np.sqrt(diag[idx])
        else:
            arr = arr.reshape(-1)
    else:
        arr = arr.reshape(-1)

    if dims is None or int(np.prod(dims, dtype=int)) != arr.size:
        n = int(np.log2(arr.size)) if arr.size > 0 else 0
        if 2 ** n == arr.size:
            dims = tuple([2] * n)
        else:
            dims = (arr.size,)

    num_subsystems = len(dims)

    if qargs_B is None:
        qargs_B = list(range(num_subsystems))
    elif isinstance(qargs_B, (int, np.integer)):
        qargs_B = [int(qargs_B)]
    else:
        qargs_B = [int(q) for q in qargs_B]

    qargs_B = sorted(qargs_B)

    if len(set(qargs_B)) != len(qargs_B):
        raise ValueError("Duplicate subsystem arguments are not allowed.")
    if any(q < 0 or q >= num_subsystems for q in qargs_B):
        raise ValueError("Subsystem argument out of range.")

    qargs_A = [q for q in range(num_subsystems) if q not in set(qargs_B)]

    dims_A = [dims[q] for q in qargs_A]
    dims_B = [dims[q] for q in qargs_B]

    dim_A = int(np.prod(dims_A, dtype=int)) if dims_A else 1
    dim_B = int(np.prod(dims_B, dtype=int)) if dims_B else 1

    tensor = arr.reshape(tuple(reversed(dims)))
    axes_A = [num_subsystems - 1 - q for q in reversed(qargs_A)]
    axes_B = [num_subsystems - 1 - q for q in reversed(qargs_B)]
    matrix = np.transpose(tensor, axes_A + axes_B).reshape(dim_A, dim_B)

    u, s, vh = np.linalg.svd(matrix, full_matrices=False)

    result = []
    for i, coeff in enumerate(s):
        if np.isclose(coeff, 0.0):
            break
        result.append((coeff, np.array(u[:, i], dtype=complex), np.array(vh[i, :], dtype=complex)))

    return result
