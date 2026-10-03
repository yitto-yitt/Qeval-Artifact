# EVAL_META: task_id=139, framework=cirq, class=2
import cirq
import numpy as np


def schmidt_test(data, qargs_B):
    dims_method = getattr(data, "dims", None)
    dims = tuple(dims_method()) if callable(dims_method) else None

    if isinstance(data, (np.ndarray, list, tuple)):
        array = np.asarray(data, dtype=np.complex128)
    else:
        array = np.asarray(getattr(data, "data", data), dtype=np.complex128)

    if array.ndim == 1:
        state = array
    elif array.ndim == 2 and array.shape[1] == 1:
        state = array[:, 0]
    elif array.ndim == 2 and array.shape[0] == array.shape[1]:
        if not np.allclose(array, array.conj().T, atol=1e-8, rtol=1e-5):
            raise ValueError("Density matrix is not Hermitian.")
        state = cirq.density_matrix_to_state_vector(array, atol=1e-8)
        if not np.allclose(
            np.outer(state, state.conj()), array, atol=1e-8, rtol=1e-5
        ):
            raise ValueError("Density matrix is not a pure state.")
    else:
        raise ValueError("Expected a state vector or a square density matrix.")

    size = state.size
    if size == 0:
        raise ValueError("The state must not be empty.")

    if dims is None:
        if size & (size - 1) == 0:
            dims = (2,) * (size.bit_length() - 1)
        else:
            dims = (size,)

    if int(np.prod(dims)) != size:
        raise ValueError("Subsystem dimensions do not match the state.")

    subsystem_count = len(dims)
    partition_b = list(qargs_B)
    if any(
        not isinstance(index, (int, np.integer))
        or index < 0
        or index >= subsystem_count
        for index in partition_b
    ):
        raise ValueError("Invalid subsystem index.")
    if len(set(partition_b)) != len(partition_b):
        raise ValueError("Subsystem indices must be distinct.")

    partition_b = sorted(partition_b, reverse=True)
    partition_a = [
        index
        for index in range(subsystem_count - 1, -1, -1)
        if index not in partition_b
    ]
    if not partition_a or not partition_b:
        raise ValueError("Both Schmidt subsystems must be nonempty.")

    axes = [
        subsystem_count - 1 - index
        for index in partition_a + partition_b
    ]
    dimension_a = int(np.prod([dims[index] for index in partition_a]))
    dimension_b = int(np.prod([dims[index] for index in partition_b]))
    matrix = state.reshape(dims[::-1]).transpose(axes).reshape(
        dimension_a, dimension_b
    )

    vectors_a, coefficients, vectors_b = np.linalg.svd(
        matrix, full_matrices=False
    )
    return [
        (float(coefficient), vectors_a[:, index].copy(), vectors_b[index].copy())
        for index, coefficient in enumerate(coefficients)
        if not np.isclose(coefficient, 0)
    ]
