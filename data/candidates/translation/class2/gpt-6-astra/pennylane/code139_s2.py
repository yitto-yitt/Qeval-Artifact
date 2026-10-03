# EVAL_META: task_id=139, framework=pennylane, class=2
import numpy as np
import pennylane as qml


def schmidt_test(data, qargs_B):
    dims_method = getattr(data, "dims", None)
    dims = tuple(dims_method()) if callable(dims_method) else None
    raw = data.data if callable(dims_method) and hasattr(data, "data") else data
    state = np.asarray(raw, dtype=complex)
    atol, rtol = 1e-8, 1e-5

    if state.ndim == 2 and state.shape[1] == 1:
        state = state[:, 0]
    elif state.ndim == 2:
        if state.shape[0] != state.shape[1]:
            raise ValueError("The density matrix must be square.")
        if not np.allclose(state, state.conj().T, atol=atol, rtol=rtol):
            raise ValueError("The density matrix must be Hermitian.")
        values, vectors = np.linalg.eig(state)
        order = np.argsort(values)
        values, vectors = values[order], vectors[:, order]
        if not (
            np.allclose(values[:-1], 0, atol=atol, rtol=rtol)
            and np.isclose(values[-1], 1, atol=atol, rtol=rtol)
        ):
            raise ValueError("Schmidt decomposition requires a pure state.")
        state = vectors[:, -1]
    elif state.ndim != 1:
        raise ValueError("Expected a state vector or density matrix.")

    if state.size == 0 or not np.isclose(
        np.linalg.norm(state), 1, atol=atol, rtol=rtol
    ):
        raise ValueError("The state must be normalized.")

    if dims is None:
        size = state.size
        dims = (2,) * (size.bit_length() - 1) if size & (size - 1) == 0 else (size,)
    if np.prod(dims, dtype=int) != state.size:
        raise ValueError("Subsystem dimensions do not match the state.")

    subsystem_B = sorted(qargs_B)
    count = len(dims)
    if (
        len(set(subsystem_B)) != len(subsystem_B)
        or any(not isinstance(i, (int, np.integer)) or i < 0 or i >= count
               for i in subsystem_B)
    ):
        raise ValueError("Invalid subsystem indices.")
    subsystem_A = [i for i in range(count) if i not in subsystem_B]
    if not subsystem_A or not subsystem_B:
        raise ValueError("Both parts of the partition must be nonempty.")

    axes = [count - 1 - i for i in subsystem_A[::-1] + subsystem_B[::-1]]
    tensor = qml.math.reshape(state, dims[::-1])
    tensor = qml.math.transpose(tensor, axes)
    size_A = int(np.prod([dims[i] for i in subsystem_A]))
    size_B = int(np.prod([dims[i] for i in subsystem_B]))
    matrix = qml.math.reshape(tensor, (size_A, size_B))
    left, coefficients, right = np.linalg.svd(matrix)

    return [
        (coefficient, left[:, i].copy(), right[i, :].copy())
        for i, coefficient in enumerate(coefficients)
        if not np.isclose(coefficient, 0)
    ]
