# EVAL_META: task_id=139, framework=qpanda, class=2
import numpy as np
import pyqpanda3.core as pq

def schmidt_test(data, qargs_B):
    def _as_array_and_dims(obj):
        dims = None
        if hasattr(obj, "dims") and callable(getattr(obj, "dims")):
            try:
                dims = tuple(int(x) for x in obj.dims())
            except Exception:
                dims = None
        if isinstance(obj, np.ndarray):
            arr = np.asarray(obj, dtype=complex)
        elif hasattr(obj, "data"):
            try:
                arr = np.asarray(obj.data, dtype=complex)
            except Exception:
                arr = np.asarray(obj, dtype=complex)
        else:
            arr = np.asarray(obj, dtype=complex)
        return arr, dims

    def _infer_qubit_dims(length):
        if length <= 0:
            raise ValueError("Invalid state dimension.")
        n = int(round(np.log2(length)))
        if 2 ** n == length:
            return (2,) * n
        return (length,)

    def _digits_from_index(index, dims):
        out = []
        for d in dims:
            out.append(index % d)
            index //= d
        return out

    def _sub_index(digits, qargs, dims):
        idx = 0
        stride = 1
        for q in qargs:
            idx += digits[q] * stride
            stride *= dims[q]
        return idx

    arr, dims = _as_array_and_dims(data)

    if arr.ndim == 2 and 1 in arr.shape:
        arr = arr.reshape(-1)
    elif arr.ndim == 2 and arr.shape[0] == arr.shape[1]:
        vals, vecs = np.linalg.eigh(arr)
        pos = int(np.argmax(np.abs(vals)))
        val = vals[pos]
        vec = vecs[:, pos]
        if np.real(val) > 0:
            vec = np.sqrt(np.real(val)) * vec
        arr = vec
    elif arr.ndim != 1:
        arr = arr.reshape(-1)

    state = np.asarray(arr, dtype=complex).reshape(-1)

    if dims is None or int(np.prod(dims, dtype=int)) != state.size:
        dims = _infer_qubit_dims(state.size)

    num_subsystems = len(dims)
    qargs_B = sorted(int(q) for q in qargs_B)

    if len(set(qargs_B)) != len(qargs_B):
        raise ValueError("Duplicate subsystem indices in qargs_B.")
    if any(q < 0 or q >= num_subsystems for q in qargs_B):
        raise ValueError("Subsystem index out of range.")
    if len(qargs_B) == 0 or len(qargs_B) == num_subsystems:
        raise ValueError("Schmidt decomposition requires a non-trivial bipartition.")

    qargs_A = [q for q in range(num_subsystems) if q not in qargs_B]

    dim_A = int(np.prod([dims[q] for q in qargs_A], dtype=int))
    dim_B = int(np.prod([dims[q] for q in qargs_B], dtype=int))

    mat = np.zeros((dim_A, dim_B), dtype=complex)
    for full_index, amp in enumerate(state):
        digits = _digits_from_index(full_index, dims)
        a_index = _sub_index(digits, qargs_A, dims)
        b_index = _sub_index(digits, qargs_B, dims)
        mat[a_index, b_index] = amp

    u, s, vh = np.linalg.svd(mat, full_matrices=False)

    return [
        (s[i], np.array(u[:, i], dtype=complex), np.array(vh[i, :], dtype=complex))
        for i in range(len(s))
        if not np.isclose(s[i], 0.0)
    ]
