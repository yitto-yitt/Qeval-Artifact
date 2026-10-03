# EVAL_META: task_id=139, framework=cirq, class=2
import numpy as np
import cirq


def schmidt_test(data, qargs_B):
    dims_method = getattr(data, "dims", None)
    dims = tuple(dims_method()) if callable(dims_method) else None
    raw = data if isinstance(data, (list, tuple, np.ndarray)) else getattr(data, "data", data)
    state = np.asarray(raw, dtype=np.complex128)
    atol, rtol = 1e-8, 1e-5

    if state.ndim == 2 and state.shape[1] == 1:
        state = state[:, 0]

    if state.ndim == 2:
        if state.shape[0] != state.shape[1]:
            raise ValueError("Density matrix must be square.")
        if not np.allclose(state, state.conj().T, atol=atol, rtol=rtol):
            raise ValueError("Density matrix must be Hermitian.")
        if not np.isclose(np.trace(state), 1, atol=atol, rtol=rtol):
            raise ValueError("Density matrix must have unit trace.")
        eigenvalues, eigenvectors = np.linalg.eigh(state)
        if np.any(eigenvalues < -atol):
            raise ValueError("Density matrix must be positive semidefinite.")
        index = int(np.argmax(eigenvalues))
        if not np.isclose(eigenvalues[index], 1, atol=atol, rtol=rtol):
            raise ValueError("Schmidt decomposition requires a pure state.")
        state = eigenvectors[:, index]
        nonzero = np.flatnonzero(np.abs(state) > atol)
        if nonzero.size:
            amplitude = state[nonzero[0]]
            state = state * np.conj(amplitude) / np.abs(amplitude)
    elif state.ndim != 1:
        raise ValueError("Expected a state vector or density matrix.")

    size = state.size
    if size == 0:
        raise ValueError("State cannot be empty.")
    if dims is None:
        dims = (2,) * (size.bit_length() - 1) if size & (size - 1) == 0 else (size,)
    if int(np.prod(dims)) != size:
        raise ValueError("Subsystem dimensions do not match the state.")

    cirq.validate_normalized_state_vector(
        state, qid_shape=dims[::-1], atol=atol
    )

    qargs_B = sorted(qargs_B)
    if any(not isinstance(q, (int, np.integer)) for q in qargs_B):
        raise ValueError("Subsystem indices must be integers.")
    if len(set(qargs_B)) != len(qargs_B):
        raise ValueError("Subsystem indices must be distinct.")
    if any(q < 0 or q >= len(dims) for q in qargs_B):
        raise ValueError("Subsystem index out of range.")

    qargs_A = [q for q in range(len(dims)) if q not in qargs_B]
    if not qargs_A or not qargs_B:
        raise ValueError("Both subsystems must be nonempty.")

    axes = [len(dims) - 1 - q for q in qargs_A[::-1] + qargs_B[::-1]]
    dim_A = int(np.prod([dims[q] for q in qargs_A]))
    dim_B = int(np.prod([dims[q] for q in qargs_B]))
    matrix = state.reshape(dims[::-1]).transpose(axes).reshape(dim_A, dim_B)
    left, coefficients, right = np.linalg.svd(matrix, full_matrices=False)

    return [
        (coefficient, left[:, index].copy(), right[index, :].copy())
        for index, coefficient in enumerate(coefficients)
        if not np.isclose(coefficient, 0)
    ]
