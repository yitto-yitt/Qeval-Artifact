# EVAL_META: task_id=139, framework=cirq, class=2
import cirq
import numpy as np


def schmidt_test(data, qargs_B):
    dims_method = getattr(data, "dims", None)
    dims = tuple(dims_method()) if callable(dims_method) else None
    raw = data if isinstance(data, (np.ndarray, list, tuple)) else getattr(data, "data", data)
    state = np.asarray(raw, dtype=np.complex128)

    if state.ndim == 2 and state.shape[1] == 1:
        state = state[:, 0]

    if state.ndim == 2:
        if state.shape[0] != state.shape[1]:
            raise ValueError("The density matrix must be square.")
        if not np.allclose(state, state.conj().T, atol=1e-8, rtol=1e-5):
            raise ValueError("The density matrix must be Hermitian.")
        eigenvalues, eigenvectors = np.linalg.eigh(state)
        if (
            not np.isclose(np.trace(state), 1, atol=1e-8, rtol=1e-5)
            or np.any(eigenvalues < -1e-8)
            or np.count_nonzero(np.abs(eigenvalues) > 1e-8) != 1
        ):
            raise ValueError("Schmidt decomposition requires a pure state.")
        state = eigenvectors[:, np.argmax(eigenvalues)]
        pivot = np.argmax(np.abs(state))
        state = state * np.exp(-1j * np.angle(state[pivot]))
    elif state.ndim != 1:
        raise ValueError("Expected a state vector or density matrix.")

    size = state.size
    if size == 0:
        raise ValueError("The state must not be empty.")
    if dims is None:
        dims = (2,) * (size.bit_length() - 1) if size & (size - 1) == 0 else (size,)
    if np.prod(dims, dtype=int) != size:
        raise ValueError("Subsystem dimensions do not match the state.")

    state = cirq.to_valid_state_vector(
        state, qid_shape=dims, dtype=np.complex128, atol=1e-5
    )

    subsystem_B = sorted(qargs_B)
    if (
        len(set(subsystem_B)) != len(subsystem_B)
        or any(not isinstance(i, (int, np.integer)) for i in subsystem_B)
        or any(i < 0 or i >= len(dims) for i in subsystem_B)
    ):
        raise ValueError("Invalid subsystem indices.")
    subsystem_A = [i for i in range(len(dims)) if i not in subsystem_B]
    if not subsystem_A or not subsystem_B:
        raise ValueError("Both subsystems must be nonempty.")

    axes = [len(dims) - 1 - i for i in subsystem_A[::-1] + subsystem_B[::-1]]
    size_A = int(np.prod([dims[i] for i in subsystem_A]))
    size_B = int(np.prod([dims[i] for i in subsystem_B]))
    matrix = state.reshape(dims[::-1]).transpose(axes).reshape(size_A, size_B)
    left, coefficients, right = np.linalg.svd(matrix, full_matrices=False)

    return [
        (float(coefficient), left[:, i].copy(), right[i, :].copy())
        for i, coefficient in enumerate(coefficients)
        if not np.isclose(coefficient, 0)
    ]
