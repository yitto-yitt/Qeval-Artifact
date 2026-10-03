# EVAL_META: task_id=139, framework=qpanda2, class=2
import numpy as np
import pyqpanda as pq

def schmidt_test(data, qargs_B):
    raw_obj = data
    dims = None

    dims_attr = getattr(raw_obj, "dims", None)
    if callable(dims_attr):
        try:
            dims = tuple(int(x) for x in dims_attr())
        except TypeError:
            dims = None

    if hasattr(raw_obj, "data") and not isinstance(raw_obj, (list, tuple, np.ndarray)):
        arr = np.asarray(raw_obj.data, dtype=complex)
    else:
        arr = np.asarray(raw_obj, dtype=complex)

    if arr.ndim == 2:
        if 1 in arr.shape and arr.shape[0] != arr.shape[1]:
            vec = arr.reshape(-1)
        elif arr.shape[0] == arr.shape[1]:
            vals, vecs = np.linalg.eigh(arr)
            idx = int(np.argmax(np.real(vals)))
            val = vals[idx]
            vec = np.sqrt(max(float(np.real_if_close(val)), 0.0)) * vecs[:, idx]
            nz = np.flatnonzero(np.abs(vec) > 1e-12)
            if nz.size:
                phase = np.exp(-1j * np.angle(vec[nz[0]]))
                vec = vec * phase
        else:
            vec = arr.reshape(-1)
    else:
        vec = arr.reshape(-1)

    total_dim = int(vec.size)

    if dims is None or int(np.prod(dims)) != total_dim:
        n_qubits = int(round(np.log2(total_dim))) if total_dim > 0 else 0
        if 2 ** n_qubits == total_dim:
            dims = tuple([2] * n_qubits)
        else:
            dims = (total_dim,)

    num_subsystems = len(dims)

    if qargs_B is None:
        qargs_B = list(range(num_subsystems // 2))
    else:
        qargs_B = list(qargs_B)

    qargs_B = sorted(int(q) for q in qargs_B)
    qargs_A = [i for i in range(num_subsystems) if i not in qargs_B]

    tensor = np.reshape(vec, tuple(reversed(dims)))

    axes_A = [num_subsystems - 1 - q for q in reversed(qargs_A)]
    axes_B = [num_subsystems - 1 - q for q in reversed(qargs_B)]
    transposed = np.transpose(tensor, axes_A + axes_B)

    dim_A = int(np.prod([dims[q] for q in qargs_A], dtype=int)) if qargs_A else 1
    dim_B = int(np.prod([dims[q] for q in qargs_B], dtype=int)) if qargs_B else 1

    matrix = np.reshape(transposed, (dim_A, dim_B))
    u, s, vh = np.linalg.svd(matrix, full_matrices=False)

    result = []
    for i, coeff in enumerate(s):
        if coeff > 1e-10:
            state_A = np.array(u[:, i], dtype=complex, copy=True)
            state_B = np.array(np.conjugate(vh[i, :]), dtype=complex, copy=True)
            result.append((coeff, state_A, state_B))

    return result
