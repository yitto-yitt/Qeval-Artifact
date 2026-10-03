# EVAL_META: task_id=139, framework=pennylane, class=2
import numpy as np
import pennylane as qml


def schmidt_test(data, qargs_B):
    dims_method = getattr(data, "dims", None)
    dims = tuple(dims_method()) if callable(dims_method) else None
    raw = data.data if callable(dims_method) else data
    state = np.asarray(raw, dtype=complex)

    if state.ndim == 2 and state.shape[0] == state.shape[1]:
        if not np.allclose(state, state.conj().T, atol=1e-8, rtol=1e-5):
            raise ValueError("The density matrix must be Hermitian.")
        eigenvalues, eigenvectors = np.linalg.eig(state)
        index = int(np.argmax(eigenvalues.real))
        if (
            not np.isclose(eigenvalues[index], 1, atol=1e-8, rtol=1e-5)
            or not np.allclose(
                np.delete(eigenvalues, index), 0, atol=1e-8, rtol=1e-5
            )
        ):
            raise ValueError("The density matrix must represent a pure state.")
        state = eigenvectors[:, index]
        state = state / np.linalg.norm(state)
    elif state.ndim == 2 and state.shape[1] == 1:
        state = state[:, 0]
    elif state.ndim != 1:
        raise ValueError("Expected a state vector or a pure density matrix.")

    size = state.size
    if size == 0 or not np.isclose(
        np.vdot(state, state), 1, atol=1e-8, rtol=1e-5
    ):
        raise ValueError("The state must be normalized.")

    if dims is None:
        dims = (
            (2,) * (size.bit_length() - 1)
            if size > 1 and size & (size - 1) == 0
            else (size,)
        )
    if int(np.prod(dims)) != size:
        raise ValueError("Subsystem dimensions do not match the state.")

    subsystem_B = sorted(set(qargs_B))
    if any(
        not isinstance(index, (int, np.integer))
        or index < 0
        or index >= len(dims)
        for index in subsystem_B
    ):
        raise ValueError("Invalid subsystem index.")
    subsystem_A = [index for index in range(len(dims)) if index not in subsystem_B]
    if not subsystem_A or not subsystem_B:
        raise ValueError("Both subsystems must be nonempty.")

    axes = [
        len(dims) - 1 - index
        for index in subsystem_A[::-1] + subsystem_B[::-1]
    ]
    dimension_A = int(np.prod([dims[index] for index in subsystem_A]))
    dimension_B = int(np.prod([dims[index] for index in subsystem_B]))
    matrix = state.reshape(dims[::-1]).transpose(axes).reshape(
        dimension_A, dimension_B
    )
    vectors_A, coefficients, vectors_B = qml.math.svd(
        matrix, full_matrices=False
    )
    return [
        (float(coefficient), vectors_A[:, index].copy(), vectors_B[index, :].copy())
        for index, coefficient in enumerate(coefficients)
        if not np.isclose(coefficient, 0)
    ]
