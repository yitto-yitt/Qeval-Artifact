# EVAL_META: task_id=139, framework=pennylane, class=2
import numpy as np


def schmidt_test(data, qargs_B):
    dims = None
    dims_method = getattr(data, "dims", None)
    if callable(dims_method):
        try:
            candidate_dims = dims_method()
            if isinstance(candidate_dims, tuple) and all(np.isscalar(x) for x in candidate_dims):
                dims = tuple(int(x) for x in candidate_dims)
        except Exception:
            dims = None

    try:
        arr = np.asarray(data, dtype=complex)
    except Exception:
        arr = np.asarray(getattr(data, "data"), dtype=complex)

    if arr.ndim == 0 and hasattr(data, "data"):
        arr = np.asarray(getattr(data, "data"), dtype=complex)

    if arr.ndim == 2:
        if arr.shape[0] != arr.shape[1]:
            raise ValueError("Input density matrix must be square.")
        vals, vecs = np.linalg.eigh(arr)
        idx = int(np.argmax(np.real(vals)))
        scale = np.sqrt(max(float(np.real(vals[idx])), 0.0))
        state = scale * vecs[:, idx]
        total_dim = arr.shape[0]
    elif arr.ndim == 1:
        state = arr.astype(complex, copy=False)
        total_dim = state.size
    else:
        raise ValueError("Input must be a state vector or density matrix.")

    if dims is None or int(np.prod(dims)) != total_dim:
        n = int(round(np.log2(total_dim))) if total_dim > 0 else 0
        if 2**n != total_dim:
            raise ValueError("Cannot infer qubit dimensions from input size.")
        dims = (2,) * n

    num_subsystems = len(dims)

    if qargs_B is None:
        qargs_B = [0]
    elif isinstance(qargs_B, (int, np.integer)):
        qargs_B = [int(qargs_B)]
    else:
        qargs_B = [int(q) for q in qargs_B]

    if len(set(qargs_B)) != len(qargs_B):
        raise ValueError("Duplicate subsystem index in qargs_B.")
    if any(q < 0 or q >= num_subsystems for q in qargs_B):
        raise ValueError("Subsystem index out of range.")

    qargs_A = [i for i in range(num_subsystems) if i not in qargs_B]

    dim_A = int(np.prod([dims[i] for i in qargs_A], dtype=int)) if qargs_A else 1
    dim_B = int(np.prod([dims[i] for i in qargs_B], dtype=int)) if qargs_B else 1

    tensor = np.reshape(state, dims, order="F")
    permuted = np.transpose(tensor, qargs_A + qargs_B) if num_subsystems else tensor
    matrix = np.reshape(permuted, (dim_A, dim_B), order="F")

    u, s, vh = np.linalg.svd(matrix, full_matrices=False)

    terms = []
    for i, coeff in enumerate(s):
        if coeff > 1e-10:
            terms.append((float(coeff), np.array(u[:, i], dtype=complex), np.array(vh[i, :], dtype=complex)))

    return terms
