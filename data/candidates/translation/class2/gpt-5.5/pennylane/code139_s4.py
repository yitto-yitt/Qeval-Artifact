# EVAL_META: task_id=139, framework=pennylane, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    if hasattr(data, "data") and not isinstance(data, np.ndarray):
        try:
            arr = np.asarray(data.data, dtype=complex)
        except Exception:
            arr = np.asarray(data, dtype=complex)
    else:
        arr = np.asarray(data, dtype=complex)

    dims = None
    if hasattr(data, "dims") and callable(getattr(data, "dims")):
        try:
            d = tuple(int(x) for x in data.dims())
            if d and np.prod(d, dtype=int) in (arr.size, arr.shape[0] if arr.ndim >= 1 else 0):
                dims = d
        except Exception:
            dims = None

    if arr.ndim == 1:
        state = arr.astype(complex, copy=False)
    elif arr.ndim == 2 and 1 in arr.shape:
        state = arr.reshape(-1).astype(complex, copy=False)
    elif arr.ndim == 2 and arr.shape[0] == arr.shape[1]:
        rho = arr.astype(complex, copy=False)
        if np.allclose(rho, rho.conj().T):
            vals, vecs = np.linalg.eigh(rho)
            idx = int(np.argmax(vals.real))
            val = max(float(vals[idx].real), 0.0)
            state = np.sqrt(val) * vecs[:, idx]
        else:
            vals, vecs = np.linalg.eig(rho)
            idx = int(np.argmax(np.abs(vals)))
            state = np.sqrt(vals[idx]) * vecs[:, idx]
    else:
        state = arr.reshape(-1).astype(complex, copy=False)

    total_dim = int(state.size)
    if dims is None or int(np.prod(dims, dtype=int)) != total_dim:
        n_float = np.log2(total_dim)
        n = int(round(n_float))
        if 2 ** n != total_dim:
            raise ValueError("Input dimension is not compatible with qubit subsystems.")
        dims = (2,) * n
    else:
        n = len(dims)

    qargs_B = [] if qargs_B is None else list(qargs_B)
    qargs_A = [q for q in range(n) if q not in qargs_B]

    def axes_for(qargs):
        return [n - 1 - q for q in reversed(qargs)]

    dim_A = int(np.prod([dims[q] for q in qargs_A], dtype=int)) if qargs_A else 1
    dim_B = int(np.prod([dims[q] for q in qargs_B], dtype=int)) if qargs_B else 1

    tensor = np.reshape(state, tuple(reversed(dims)))
    axes = axes_for(qargs_A) + axes_for(qargs_B)
    matrix = np.transpose(tensor, axes).reshape(dim_A, dim_B) if axes else tensor.reshape(dim_A, dim_B)

    u, s, vh = np.linalg.svd(matrix, full_matrices=False)
    tol = 1e-10

    return [(s[i], u[:, i], vh[i, :]) for i in range(len(s)) if s[i] > tol]
