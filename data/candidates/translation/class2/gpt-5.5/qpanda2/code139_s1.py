# EVAL_META: task_id=139, framework=qpanda2, class=2
import numpy as np
import pyqpanda as pq

def schmidt_test(data, qargs_B):
    class _StatevectorLike:
        def __init__(self, vec, dims):
            self.data = np.asarray(vec, dtype=complex)
            self._dims = tuple(int(d) for d in dims)

        def dims(self, qargs=None):
            if qargs is None:
                return self._dims
            return tuple(self._dims[int(i)] for i in qargs)

        def __array__(self, dtype=None):
            return np.asarray(self.data, dtype=dtype)

        def __len__(self):
            return len(self.data)

        def __iter__(self):
            return iter(self.data)

        def __getitem__(self, key):
            return self.data[key]

        def tolist(self):
            return self.data.tolist()

    dims = None
    if hasattr(data, "dims") and callable(getattr(data, "dims")):
        try:
            dims = tuple(int(d) for d in data.dims())
        except Exception:
            dims = None

    if isinstance(data, np.ndarray):
        arr = np.asarray(data, dtype=complex)
    else:
        raw = getattr(data, "data", None)
        if raw is not None and not isinstance(raw, (memoryview, bytes, bytearray)):
            try:
                arr = np.asarray(raw, dtype=complex)
            except Exception:
                arr = np.asarray(data, dtype=complex)
        else:
            arr = np.asarray(data, dtype=complex)

    if arr.ndim == 2 and arr.shape[0] == arr.shape[1]:
        mat = np.asarray(arr, dtype=complex)
        diag = np.diag(mat)
        k = int(np.argmax(np.abs(diag)))
        p = float(np.real(diag[k]))
        if p > 0:
            state = mat[:, k] / np.sqrt(p)
        else:
            vals, vecs = np.linalg.eigh(mat)
            state = vecs[:, int(np.argmax(vals))]
    elif arr.ndim == 2 and (arr.shape[0] == 1 or arr.shape[1] == 1):
        state = arr.reshape(-1)
    elif arr.ndim > 1:
        state = arr.reshape(-1, order="F")
    else:
        state = arr.reshape(-1)

    if dims is None or int(np.prod(dims, dtype=int)) != state.size:
        if state.size > 0 and (state.size & (state.size - 1)) == 0:
            dims = tuple(2 for _ in range(int(np.log2(state.size))))
        else:
            dims = (int(state.size),)

    qargs_B = list(qargs_B)
    qargs_B = [int(q) for q in qargs_B]
    n_subsystems = len(dims)
    if any(q < 0 or q >= n_subsystems for q in qargs_B):
        raise ValueError("qargs_B contains an invalid subsystem index")
    if len(set(qargs_B)) != len(qargs_B):
        raise ValueError("qargs_B contains duplicate subsystem indices")

    qargs_A = [i for i in range(n_subsystems) if i not in qargs_B]
    dims_A = tuple(dims[i] for i in qargs_A)
    dims_B = tuple(dims[i] for i in qargs_B)
    dim_A = int(np.prod(dims_A, dtype=int)) if dims_A else 1
    dim_B = int(np.prod(dims_B, dtype=int)) if dims_B else 1

    tensor = np.reshape(state, dims, order="F") if dims else np.asarray(state).reshape(())
    tensor = np.transpose(tensor, axes=qargs_A + qargs_B) if n_subsystems else tensor
    matrix = np.reshape(tensor, (dim_A, dim_B), order="F")

    u, s, vh = np.linalg.svd(matrix, full_matrices=False)
    tol = max(matrix.shape) * np.finfo(float).eps * (s[0] if len(s) else 0.0)

    return [
        (s[i], _StatevectorLike(u[:, i], dims_A), _StatevectorLike(np.conjugate(vh[i, :]), dims_B))
        for i in range(len(s))
        if s[i] > tol
    ]
