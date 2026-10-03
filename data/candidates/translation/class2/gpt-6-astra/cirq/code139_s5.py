# EVAL_META: task_id=139, framework=cirq, class=2
import cirq
import numpy as np


def schmidt_test(data, qargs_B):
    if isinstance(data, cirq.QuantumState):
        dims = tuple(reversed(data.qid_shape))
        array = np.asarray(data.data, dtype=complex)
    else:
        array = np.asarray(data, dtype=complex)
        if array.ndim == 2 and array.shape[1] == 1:
            array = array[:, 0]
        if array.ndim not in (1, 2) or array.shape[0] == 0:
            raise ValueError("Input must be a state vector or density matrix.")
        dimension = array.shape[0]
        if dimension & (dimension - 1) == 0:
            dims = (2,) * (dimension.bit_length() - 1)
        else:
            dims = (dimension,)

    if array.ndim == 2:
        if array.shape[0] != array.shape[1]:
            raise ValueError("A density matrix must be square.")
        if not np.allclose(array, array.conj().T, atol=1e-8, rtol=1e-5):
            raise ValueError("The density matrix must be Hermitian.")
        eigenvalues, eigenvectors = np.linalg.eigh(array)
        nonzero = eigenvalues[~np.isclose(eigenvalues, 0, atol=1e-8, rtol=1e-5)]
        if len(nonzero) != 1 or not np.isclose(
            nonzero[0], 1, atol=1e-8, rtol=1e-5
        ):
            raise ValueError("Schmidt decomposition requires a pure state.")
        state = eigenvectors[:, np.argmax(eigenvalues)].copy()
        pivot = state[np.argmax(np.abs(state))]
        state *= np.conj(pivot) / abs(pivot)
    elif array.ndim == 1:
        state = array
    else:
        raise ValueError("Input must be a state vector or density matrix.")

    if not np.isclose(np.vdot(state, state), 1, atol=1e-8, rtol=1e-5):
        raise ValueError("The state must be normalized.")

    count = len(dims)
    subsystem_B = sorted(qargs_B)
    if (
        not subsystem_B
        or len(set(subsystem_B)) != len(subsystem_B)
        or any(
            not isinstance(index, (int, np.integer))
            or index < 0
            or index >= count
            for index in subsystem_B
        )
    ):
        raise ValueError("Invalid subsystem partition.")
    subsystem_A = [index for index in range(count) if index not in subsystem_B]
    if not subsystem_A:
        raise ValueError("Both subsystems must be nonempty.")

    dimension_A = int(np.prod([dims[index] for index in subsystem_A]))
    dimension_B = int(np.prod([dims[index] for index in subsystem_B]))
    axes = [count - 1 - index for index in reversed(subsystem_A)]
    axes += [count - 1 - index for index in reversed(subsystem_B)]
    matrix = state.reshape(dims[::-1]).transpose(axes)
    matrix = matrix.reshape(dimension_A, dimension_B)
    left, coefficients, right = np.linalg.svd(matrix, full_matrices=False)

    return [
        (float(coefficient), left[:, index].copy(), right[index, :].copy())
        for index, coefficient in enumerate(coefficients)
        if not np.isclose(coefficient, 0)
    ]
