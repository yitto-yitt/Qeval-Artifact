# EVAL_META: task_id=139, framework=cirq, class=2
import numpy as np
import cirq

def schmidt_test(data, qargs_B):
    dims = None
    if hasattr(data, "dims") and callable(getattr(data, "dims")):
        try:
            dims = tuple(int(d) for d in data.dims())
        except Exception:
            dims = None
    elif hasattr(data, "qid_shape"):
        try:
            qid_shape = data.qid_shape
            dims = tuple(int(d) for d in (qid_shape() if callable(qid_shape) else qid_shape))
        except Exception:
            dims = None

    try:
        arr = np.asarray(data, dtype=complex)
    except Exception:
        if hasattr(data, "data"):
            arr = np.asarray(data.data, dtype=complex)
        elif hasattr(data, "final_state_vector"):
            arr = np.asarray(data.final_state_vector, dtype=complex)
        else:
            raise

    if arr.ndim == 2:
        if 1 in arr.shape:
            state = arr.reshape(-1)
        elif arr.shape[0] == arr.shape[1]:
            vals, vecs = np.linalg.eigh(arr)
            idx = int(np.argmax(vals.real))
            val = vals[idx].real
            state = vecs[:, idx] * np.sqrt(max(val, 0.0))
            nz = np.flatnonzero(np.abs(state) > 1e-12)
            if nz.size:
                phase = np.angle(state[nz[0]])
                state = state * np.exp(-1j * phase)
        else:
            state = arr.reshape(-1)
    else:
        state = arr.reshape(-1)

    dim = int(state.size)
    if dims is None or int(np.prod(dims, dtype=int)) != dim:
        n_float = np.log2(dim) if dim > 0 else 0
        n = int(round(n_float))
        if 2 ** n == dim:
            dims = (2,) * n
        else:
            dims = (dim,)
    else:
        n = len(dims)

    if qargs_B is None:
        qargs_B = list(range(n // 2, n))
    else:
        qargs_B = [int(q) for q in qargs_B]

    if len(set(qargs_B)) != len(qargs_B) or any(q < 0 or q >= n for q in qargs_B):
        raise ValueError("Invalid subsystem indices.")

    set_B = set(qargs_B)
    qargs_A = [q for q in range(n) if q not in set_B]

    dims_A = tuple(dims[q] for q in qargs_A)
    dims_B = tuple(dims[q] for q in qargs_B)
    dim_A = int(np.prod(dims_A, dtype=int)) if dims_A else 1
    dim_B = int(np.prod(dims_B, dtype=int)) if dims_B else 1

    tensor = np.reshape(state, dims, order="F")
    axes = qargs_A + qargs_B
    if axes:
        tensor = np.transpose(tensor, axes)
    matrix = np.reshape(tensor, (dim_A, dim_B), order="F")

    u, s, vh = np.linalg.svd(matrix, full_matrices=False)

    return [(s[i], u[:, i].copy(), vh[i, :].copy()) for i in range(len(s)) if not np.isclose(s[i], 0)]
