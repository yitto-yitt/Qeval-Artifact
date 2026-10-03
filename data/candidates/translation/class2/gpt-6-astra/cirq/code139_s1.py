# EVAL_META: task_id=139, framework=cirq, class=2
import numpy as np
import cirq


def schmidt_test(data, qargs_B):
    atol = 1e-8
    rtol = 1e-5
    dims_method = getattr(data, "dims", None)
    dims = tuple(dims_method()) if callable(dims_method) else None
    raw = data.data if callable(dims_method) else data
    array = np.asarray(raw, dtype=np.complex128)

    if array.ndim == 2 and array.shape[1] == 1:
        array = array.reshape(-1)

    if array.ndim == 1:
        vector = array.copy()
    elif array.ndim == 2 and array.shape[0] == array.shape[1]:
        if not np.allclose(array, array.conj().T, atol=atol, rtol=rtol):
            raise ValueError("The density matrix must be Hermitian.")
        if not np.isclose(np.trace(array), 1, atol=atol, rtol=rtol):
            raise ValueError("The density matrix must have unit trace.")
        eigenvalues, eigenvectors = np.linalg.eig(array)
        nonzero = np.flatnonzero(np.abs(eigenvalues) > atol)
        if len(nonzero) != 1 or not np.isclose(
            eigenvalues[nonzero[0]], 1, atol=atol, rtol=rtol
        ):
            raise ValueError("Schmidt decomposition requires a pure state.")
        vector = eigenvectors[:, nonzero[0]]
    else:
        raise ValueError("Expected a state vector or a square density matrix.")

    size = vector.size
    if size == 0:
        raise ValueError("The state must not be empty.")
    if dims is None:
        dims = (2,) * (size.bit_length() - 1) if size & (size - 1) == 0 else (size,)
    if np.prod(dims, dtype=int) != size:
        raise ValueError("Subsystem dimensions do not match the state.")
    if not np.isclose(np.vdot(vector, vector), 1, atol=atol, rtol=rtol):
        raise ValueError("The state vector must be normalized.")

    vector = cirq.to_valid_state_vector(
        vector, qid_shape=dims[::-1], dtype=np.complex128, atol=atol + rtol
    )

    qargs_B = list(qargs_B)
    count = len(dims)
    if (
        not qargs_B
        or len(qargs_B) >= count
        or len(set(qargs_B)) != len(qargs_B)
        or any(not isinstance(q, (int, np.integer)) or q < 0 or q >= count for q in qargs_B)
    ):
        raise ValueError("qargs_B must specify a nonempty proper subsystem.")

    qargs_B = sorted(qargs_B)
    qargs_A = [q for q in range(count) if q not in qargs_B]
    axes = [count - 1 - q for q in qargs_A[::-1] + qargs_B[::-1]]
    dim_A = int(np.prod([dims[q] for q in qargs_A]))
    dim_B = int(np.prod([dims[q] for q in qargs_B]))
    matrix = vector.reshape(dims[::-1]).transpose(axes).reshape(dim_A, dim_B)
    u, coefficients, vh = np.linalg.svd(matrix, full_matrices=False)

    return [
        (float(coefficient), u[:, i].copy(), vh[i, :].copy())
        for i, coefficient in enumerate(coefficients)
        if coefficient > atol
    ]
