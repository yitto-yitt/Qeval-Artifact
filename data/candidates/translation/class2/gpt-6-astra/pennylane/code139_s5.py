# EVAL_META: task_id=139, framework=pennylane, class=2
import numpy as np
import pennylane as qml

def schmidt_test(data, qargs_B):
    atol, rtol = 1e-8, 1e-5
    dims_method = getattr(data, "dims", None)
    dims = tuple(dims_method()) if callable(dims_method) else None
    raw = data.data if callable(dims_method) else data
    array = np.asarray(qml.math.toarray(raw), dtype=complex)

    if array.ndim == 1:
        state = array
        if not np.isclose(np.linalg.norm(state), 1.0, atol=atol, rtol=rtol):
            raise ValueError("The statevector must be normalized.")
    elif array.ndim == 2 and array.shape[0] == array.shape[1]:
        if not np.allclose(array, array.conj().T, atol=atol, rtol=rtol):
            raise ValueError("The density matrix must be Hermitian.")
        eigenvalues, eigenvectors = np.linalg.eigh(array)
        nonzero = eigenvalues[np.abs(eigenvalues) > atol]
        if (
            len(nonzero) != 1
            or not np.isclose(nonzero[0], 1.0, atol=atol, rtol=rtol)
        ):
            raise ValueError("Schmidt decomposition requires a pure state.")
        state = eigenvectors[:, np.argmax(eigenvalues)]
        first = np.flatnonzero(np.abs(state) > atol)[0]
        state = state * np.exp(-1j * np.angle(state[first]))
    else:
        raise ValueError("Expected a statevector or a square density matrix.")

    size = state.size
    if size == 0:
        raise ValueError("The state must not be empty.")
    if dims is None:
        dims = (2,) * (size.bit_length() - 1) if size & (size - 1) == 0 else (size,)
    if np.prod(dims, dtype=int) != size:
        raise ValueError("Subsystem dimensions do not match the state.")

    count = len(dims)
    subsystem_b = sorted(qargs_B)
    if (
        not subsystem_b
        or len(subsystem_b) == count
        or len(set(subsystem_b)) != len(subsystem_b)
        or any(not isinstance(i, (int, np.integer)) or i < 0 or i >= count
               for i in subsystem_b)
    ):
        raise ValueError("qargs_B must specify a nonempty proper subsystem.")

    subsystem_a = [i for i in range(count) if i not in subsystem_b]
    axes_a = [count - 1 - i for i in reversed(subsystem_a)]
    axes_b = [count - 1 - i for i in reversed(subsystem_b)]
    dimension_a = int(np.prod([dims[i] for i in subsystem_a]))
    dimension_b = int(np.prod([dims[i] for i in subsystem_b]))

    tensor = state.reshape(tuple(reversed(dims)))
    matrix = tensor.transpose(axes_a + axes_b).reshape(dimension_a, dimension_b)
    left, coefficients, right = np.linalg.svd(matrix)

    return [
        (coefficient, left[:, index].copy(), right[index, :].copy())
        for index, coefficient in enumerate(coefficients)
        if coefficient > atol
    ]
