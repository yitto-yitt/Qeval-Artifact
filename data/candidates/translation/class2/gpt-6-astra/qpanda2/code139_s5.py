# EVAL_META: task_id=139, framework=qpanda2, class=2
import numpy as np
import pyqpanda as pq


def schmidt_test(data, qargs_B):
    dims_method = getattr(data, "dims", None)
    raw = data if isinstance(data, (list, tuple, np.ndarray)) else getattr(data, "data", data)
    array = np.asarray(raw, dtype=complex)
    atol, rtol = 1e-8, 1e-5

    if array.ndim == 2 and array.shape[1] == 1:
        array = array[:, 0]

    if array.ndim == 1:
        state = array.copy()
    elif array.ndim == 2 and array.shape[0] == array.shape[1]:
        if not np.allclose(array, array.conj().T, atol=atol, rtol=rtol):
            raise ValueError("The density matrix must be Hermitian.")
        eigenvalues, eigenvectors = np.linalg.eig(array)
        index = int(np.argmax(eigenvalues.real))
        if not (
            np.isclose(eigenvalues[index], 1, atol=atol, rtol=rtol)
            and np.allclose(
                np.delete(eigenvalues, index), 0, atol=atol, rtol=rtol
            )
        ):
            raise ValueError("The density matrix must describe a pure state.")
        state = eigenvectors[:, index]
    else:
        raise ValueError("Expected a statevector or a square density matrix.")

    size = state.size
    if size == 0 or not np.all(np.isfinite(state)):
        raise ValueError("Invalid quantum state.")
    if not np.isclose(np.vdot(state, state), 1, atol=atol, rtol=rtol):
        raise ValueError("The quantum state must be normalized.")

    if callable(dims_method):
        dims = tuple(int(d) for d in dims_method())
    elif size & (size - 1) == 0:
        dims = (2,) * (size.bit_length() - 1)
    else:
        dims = (size,)

    if np.prod(dims, dtype=int) != size:
        raise ValueError("Subsystem dimensions do not match the state.")

    subsystem_b = sorted(qargs_B)
    if (
        not subsystem_b
        or len(subsystem_b) >= len(dims)
        or len(set(subsystem_b)) != len(subsystem_b)
        or any(i < 0 or i >= len(dims) for i in subsystem_b)
    ):
        raise ValueError("The partition must specify a proper nonempty subsystem.")
    subsystem_a = [i for i in range(len(dims)) if i not in subsystem_b]

    norm = float(np.linalg.norm(state))
    qubit_count = max(1, (size - 1).bit_length())
    dimension = 1 << qubit_count
    prepared = np.zeros(dimension, dtype=complex)
    prepared[:size] = state / norm

    phase = prepared[0] / abs(prepared[0]) if abs(prepared[0]) else 1.0
    difference = -np.conj(phase) * prepared
    difference[0] += 1.0
    denominator = float(np.vdot(difference, difference).real)
    unitary = np.eye(dimension, dtype=complex)
    if denominator > 0:
        unitary -= 2.0 * np.outer(difference, difference.conj()) / denominator
    unitary *= phase

    machine = pq.CPUQVM()
    machine.init_qvm()
    try:
        qubits = machine.qAlloc_many(qubit_count)
        program = pq.QProg()
        program << pq.QOracle(qubits, unitary.ravel().tolist())
        machine.directly_run(program)
        simulated = np.asarray(machine.get_qstate(), dtype=complex)[:size] * norm
    finally:
        machine.finalize()

    axes = [
        len(dims) - 1 - i
        for i in subsystem_a[::-1] + subsystem_b[::-1]
    ]
    dimension_a = int(np.prod([dims[i] for i in subsystem_a]))
    dimension_b = int(np.prod([dims[i] for i in subsystem_b]))
    matrix = simulated.reshape(dims[::-1]).transpose(axes)
    matrix = matrix.reshape(dimension_a, dimension_b)

    left, coefficients, right = np.linalg.svd(matrix, full_matrices=False)
    return [
        (float(coefficient), left[:, i].copy(), right[i, :].copy())
        for i, coefficient in enumerate(coefficients)
        if not np.isclose(coefficient, 0)
    ]
