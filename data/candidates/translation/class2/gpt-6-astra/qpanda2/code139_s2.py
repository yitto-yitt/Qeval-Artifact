# EVAL_META: task_id=139, framework=qpanda2, class=2
import numpy as np
import pyqpanda as pq


def schmidt_test(data, qargs_B):
    raw = data if isinstance(data, (list, tuple, np.ndarray)) else getattr(data, "data", data)
    state = np.asarray(raw, dtype=complex)

    if state.ndim == 2:
        if state.shape[0] != state.shape[1]:
            raise ValueError("The density matrix must be square.")
        if not np.allclose(state, state.conj().T):
            raise ValueError("The density matrix must be Hermitian.")
        eigenvalues, eigenvectors = np.linalg.eigh(state)
        vector = eigenvectors[:, np.argmax(eigenvalues)]
        if not np.allclose(state, np.outer(vector, vector.conj())):
            raise ValueError("Schmidt decomposition requires a pure state.")
        vector *= np.exp(-1j * np.angle(vector[np.argmax(np.abs(vector))]))
    elif state.ndim == 1:
        vector = state.copy()
    else:
        raise ValueError("Expected a statevector or a pure-state density matrix.")

    size = vector.size
    if size == 0 or not np.allclose(np.vdot(vector, vector), 1.0):
        raise ValueError("The state must be normalized.")

    dims_method = getattr(data, "dims", None)
    if callable(dims_method):
        dims = tuple(dims_method())
    elif size > 1 and size & (size - 1) == 0:
        dims = (2,) * (size.bit_length() - 1)
    else:
        dims = (size,)

    if np.prod(dims) != size:
        raise ValueError("Subsystem dimensions do not match the state.")

    subsystem_count = len(dims)
    indices_B = list(qargs_B)
    if any(not isinstance(i, (int, np.integer)) for i in indices_B):
        raise ValueError("Subsystem indices must be integers.")
    if len(set(indices_B)) != len(indices_B):
        raise ValueError("Subsystem indices must be distinct.")
    if any(i < 0 or i >= subsystem_count for i in indices_B):
        raise ValueError("Subsystem index out of range.")

    indices_B = sorted(indices_B)
    indices_A = [i for i in range(subsystem_count) if i not in indices_B]
    if not indices_A or not indices_B:
        raise ValueError("The partition must contain two nonempty subsystems.")

    qubit_count = max(1, (size - 1).bit_length())
    initial_state = np.zeros(1 << qubit_count, dtype=complex)
    initial_state[:size] = vector

    machine = pq.CPUQVM()
    machine.init_qvm()
    try:
        qubits = machine.qAlloc_many(qubit_count)
        machine.init_state(initial_state.tolist(), qubits)
        program = pq.QProg()
        program << pq.I(qubits[0])
        machine.directly_run(program)
        simulated_state = np.asarray(machine.get_qstate(), dtype=complex)[:size]
    finally:
        machine.finalize()

    axes = [
        subsystem_count - 1 - i
        for i in list(reversed(indices_A)) + list(reversed(indices_B))
    ]
    dimension_A = int(np.prod([dims[i] for i in indices_A]))
    dimension_B = int(np.prod([dims[i] for i in indices_B]))
    matrix = simulated_state.reshape(tuple(reversed(dims))).transpose(axes)
    matrix = matrix.reshape(dimension_A, dimension_B)
    vectors_A, coefficients, vectors_B = np.linalg.svd(matrix, full_matrices=False)

    return [
        (float(coefficient), vectors_A[:, i].copy(), vectors_B[i, :].copy())
        for i, coefficient in enumerate(coefficients)
        if not np.isclose(coefficient, 0)
    ]
