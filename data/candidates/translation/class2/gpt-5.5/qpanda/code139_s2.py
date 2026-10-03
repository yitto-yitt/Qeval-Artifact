# EVAL_META: task_id=139, framework=qpanda, class=2
import numpy as np
import pyqpanda3.core as pq

def schmidt_test(data, qargs_B):
    dims = None

    if hasattr(data, "dims") and callable(getattr(data, "dims")):
        try:
            dims = tuple(int(x) for x in data.dims())
        except Exception:
            dims = None

    raw = data.data if hasattr(data, "data") else data
    arr = np.asarray(raw, dtype=complex)

    if arr.ndim == 2:
        if 1 in arr.shape:
            vec = arr.reshape(-1)
        elif arr.shape[0] == arr.shape[1]:
            vals, vecs = np.linalg.eigh(arr)
            idx = int(np.argmax(vals.real))
            scale = np.sqrt(max(float(vals[idx].real), 0.0))
            vec = vecs[:, idx] * scale
        else:
            vec = arr.reshape(-1)
    else:
        vec = arr.reshape(-1)

    dim_total = int(vec.size)

    if dims is None or int(np.prod(dims, dtype=int)) != dim_total:
        if dim_total == 1:
            dims = ()
        else:
            n = int(round(np.log2(dim_total)))
            if 2 ** n == dim_total:
                dims = tuple([2] * n)
            else:
                dims = (dim_total,)

    num_subsystems = len(dims)
    qargs_B = list(qargs_B)
    qargs_A = [i for i in range(num_subsystems) if i not in set(qargs_B)]

    dim_A = int(np.prod([dims[i] for i in qargs_A], dtype=int)) if qargs_A else 1
    dim_B = int(np.prod([dims[i] for i in qargs_B], dtype=int)) if qargs_B else 1

    mat = np.zeros((dim_A, dim_B), dtype=complex)

    strides = [1]
    for d in dims[:-1]:
        strides.append(strides[-1] * int(d))

    for full_index, amp in enumerate(vec):
        a_index = 0
        a_stride = 1
        for q in qargs_A:
            digit = (full_index // strides[q]) % dims[q]
            a_index += digit * a_stride
            a_stride *= dims[q]

        b_index = 0
        b_stride = 1
        for q in qargs_B:
            digit = (full_index // strides[q]) % dims[q]
            b_index += digit * b_stride
            b_stride *= dims[q]

        mat[a_index, b_index] = amp

    u, s, vh = np.linalg.svd(mat, full_matrices=False)

    return [
        (float(s[i]), u[:, i].copy(), vh[i, :].copy())
        for i in range(len(s))
        if not np.isclose(s[i], 0.0)
    ]
