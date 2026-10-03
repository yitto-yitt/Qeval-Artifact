# EVAL_META: task_id=139, framework=pennylane, class=2
import numpy as np
import pennylane as qml


def schmidt_test(data, qargs_B):
    state = np.asarray(data, dtype=complex)

    if state.ndim == 2:
        if state.shape[0] != state.shape[1]:
            raise ValueError("The density matrix must be square.")
        if not np.allclose(state, state.conj().T, atol=1e-8, rtol=1e-5):
            raise ValueError("The density matrix must be Hermitian.")
        if not np.isclose(np.trace(state), 1, atol=1e-8, rtol=1e-5):
            raise ValueError("The density matrix must have unit trace.")

        eigenvalues, eigenvectors = np.linalg.eig(state)
        eigenvalues = eigenvalues.real
        if np.any(eigenvalues < -1e-8):
            raise ValueError("The density matrix must be positive semidefinite.")
        if np.count_nonzero(np.abs(eigenvalues) > 1e-8) != 1:
            raise ValueError("Schmidt decomposition requires a pure state.")
        state = eigenvectors[:, np.argmax(eigenvalues)]
    elif state.ndim != 1:
        raise ValueError("Expected a statevector or density matrix.")

    dimension = state.size
    if dimension == 0:
        raise ValueError("The state must not be empty.")

    if dimension & (dimension - 1) == 0:
        dims = (2,) * (dimension.bit_length() - 1)
    else:
        dims = (dimension,)

    qargs_B = sorted(qargs_B)
    if len(set(qargs_B)) != len(qargs_B):
        raise ValueError("Subsystem indices must be distinct.")
    if any(not isinstance(q, (int, np.integer)) or q < 0 or q >= len(dims)
           for q in qargs_B):
        raise ValueError("Invalid subsystem index.")

    qargs_A = [q for q in range(len(dims)) if q not in qargs_B]
    dim_A = int(np.prod([dims[q] for q in qargs_A]))
    dim_B = int(np.prod([dims[q] for q in qargs_B]))
    if dim_A == 1 or dim_B == 1:
        raise ValueError("Both Schmidt subsystems must be nontrivial.")

    axes = [
        len(dims) - 1 - q
        for q in list(reversed(qargs_A)) + list(reversed(qargs_B))
    ]
    tensor = qml.math.reshape(state, dims[::-1])
    matrix = qml.math.reshape(qml.math.transpose(tensor, axes), (dim_A, dim_B))
    vectors_A, coefficients, vectors_B = qml.math.svd(
        matrix, full_matrices=False
    )

    return [
        (float(coefficient), vectors_A[:, i].copy(), vectors_B[i, :].copy())
        for i, coefficient in enumerate(coefficients)
        if not np.isclose(coefficient, 0)
    ]
