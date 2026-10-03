# EVAL_META: task_id=139, framework=pennylane, class=2
import numpy as np
import pennylane as qml


def schmidt_test(data, qargs_B):
    atol, rtol = 1e-8, 1e-5
    array = np.asarray(qml.math.toarray(data), dtype=complex)

    if array.ndim == 2 and array.shape[1] == 1:
        array = array[:, 0]

    if array.ndim == 1:
        state = array
        if not np.isclose(np.vdot(state, state), 1.0, atol=atol, rtol=rtol):
            raise ValueError("The statevector must be normalized.")
    elif array.ndim == 2 and array.shape[0] == array.shape[1]:
        if not np.allclose(array, array.conj().T, atol=atol, rtol=rtol):
            raise ValueError("The density matrix must be Hermitian.")
        eigenvalues, eigenvectors = np.linalg.eigh(array)
        index = int(np.argmax(eigenvalues))
        state = eigenvectors[:, index]
        if not np.allclose(
            array, np.outer(state, state.conj()), atol=atol, rtol=rtol
        ):
            raise ValueError("Schmidt decomposition requires a pure state.")
    else:
        raise ValueError("Expected a statevector or a square density matrix.")

    dimension = state.size
    if dimension == 0:
        raise ValueError("The state must not be empty.")

    if dimension & (dimension - 1) == 0:
        dims = (2,) * (dimension.bit_length() - 1)
    else:
        dims = (dimension,)

    qargs_B = sorted(qargs_B)
    if (
        any(not isinstance(q, (int, np.integer)) for q in qargs_B)
        or len(set(qargs_B)) != len(qargs_B)
        or any(q < 0 or q >= len(dims) for q in qargs_B)
    ):
        raise ValueError("Invalid subsystem indices.")

    qargs_A = [q for q in range(len(dims)) if q not in qargs_B]
    if not qargs_A or not qargs_B:
        raise ValueError("The partition must contain two nonempty subsystems.")

    dim_A = int(np.prod([dims[q] for q in qargs_A]))
    dim_B = int(np.prod([dims[q] for q in qargs_B]))
    axes = [
        len(dims) - 1 - q
        for q in qargs_A[::-1] + qargs_B[::-1]
    ]
    matrix = state.reshape(dims[::-1]).transpose(axes).reshape(dim_A, dim_B)
    vectors_A, coefficients, vectors_B = np.linalg.svd(
        matrix, full_matrices=False
    )

    return [
        (float(coefficient), vectors_A[:, i].copy(), vectors_B[i, :].copy())
        for i, coefficient in enumerate(coefficients)
        if coefficient > atol
    ]
