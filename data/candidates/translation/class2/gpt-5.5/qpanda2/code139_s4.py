# EVAL_META: task_id=139, framework=qpanda2, class=2
import numpy as np
import pyqpanda as pq

def schmidt_test(data, qargs_B):
    if hasattr(data, "data"):
        arr = np.asarray(data.data, dtype=complex)
    elif hasattr(data, "to_matrix"):
        arr = np.asarray(data.to_matrix(), dtype=complex)
    else:
        arr = np.asarray(data, dtype=complex)

    dims = None
    if hasattr(data, "dims") and callable(data.dims):
        try:
            dims = tuple(int(x) for x in data.dims())
        except Exception:
            dims = None

    if arr.ndim == 2:
        if arr.shape[0] == 1 or arr.shape[1] == 1:
            state = arr.reshape(-1).astype(complex)
        elif arr.shape[0] == arr.shape[1]:
            vals, vecs = np.linalg.eigh(arr)
            state = vecs[:, int(np.argmax(vals.real))].astype(complex)
            nz = np.flatnonzero(np.abs(state) > 1e-12)
            if nz.size:
                phase = state[nz[0]] / abs(state[nz[0]])
                state = state / phase
        else:
            state = arr.reshape(-1).astype(complex)
    else:
        state = arr.reshape(-1).astype(complex)

    dim = int(state.size)
    if dims is None or int(np.prod(dims)) != dim:
        n_float = np.log2(dim)
        n = int(round(n_float))
        if 2 ** n != dim:
            raise ValueError("Input state dimension is not a power of 2.")
        dims = (2,) * n
    else:
        n = len(dims)

    qargs_B = list(qargs_B)
    if len(set(qargs_B)) != len(qargs_B):
        raise ValueError("Duplicate subsystem index in qargs_B.")
    if any(q < 0 or q >= n for q in qargs_B):
        raise ValueError("Subsystem index out of range.")

    qargs_A = [q for q in range(n) if q not in qargs_B]

    dim_A = int(np.prod([dims[q] for q in qargs_A])) if qargs_A else 1
    dim_B = int(np.prod([dims[q] for q in qargs_B])) if qargs_B else 1

    mat = np.zeros((dim_A, dim_B), dtype=complex)

    strides = [1] * n
    for i in range(1, n):
        strides[i] = strides[i - 1] * dims[i]

    mult_A = [1] * len(qargs_A)
    for i in range(1, len(qargs_A)):
        mult_A[i] = mult_A[i - 1] * dims[qargs_A[i - 1]]

    mult_B = [1] * len(qargs_B)
    for i in range(1, len(qargs_B)):
        mult_B[i] = mult_B[i - 1] * dims[qargs_B[i - 1]]

    for full_index, amp in enumerate(state):
        a_index = 0
        b_index = 0
        for j, q in enumerate(qargs_A):
            a_index += ((full_index // strides[q]) % dims[q]) * mult_A[j]
        for j, q in enumerate(qargs_B):
            b_index += ((full_index // strides[q]) % dims[q]) * mult_B[j]
        mat[a_index, b_index] = amp

    u, s, vh = np.linalg.svd(mat, full_matrices=False)

    return [(s[i], u[:, i], vh[i, :]) for i in range(len(s))]
