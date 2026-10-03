# EVAL_META: task_id=139, framework=qpanda2, class=2
import numpy as np
import pyqpanda as pq


def schmidt_test(data, qargs_B):
    array = np.asarray(data, dtype=complex)
    atol, rtol = 1e-8, 1e-5

    if array.ndim == 1:
        state = array.copy()
        if not np.isclose(np.vdot(state, state), 1, atol=atol, rtol=rtol):
            raise ValueError("The statevector is not normalized.")
    elif array.ndim == 2 and array.shape[0] == array.shape[1]:
        if not np.allclose(array, array.conj().T, atol=atol, rtol=rtol):
            raise ValueError("The density matrix is not Hermitian.")
        if not np.isclose(np.trace(array), 1, atol=atol, rtol=rtol):
            raise ValueError("The density matrix does not have unit trace.")
        eigenvalues, eigenvectors = np.linalg.eigh(array)
        if (
            not np.isclose(eigenvalues[-1], 1, atol=atol, rtol=rtol)
            or not np.allclose(eigenvalues[:-1], 0, atol=atol, rtol=rtol)
        ):
            raise ValueError("Schmidt decomposition requires a pure state.")
        state = eigenvectors[:, -1]
    else:
        raise ValueError("Expected a statevector or a square density matrix.")

    dimension = state.size
    if dimension == 0:
        raise ValueError("The state cannot be empty.")

    dims_method = getattr(data, "dims", None)
    if callable(dims_method):
        dims = tuple(int(d) for d in dims_method())
    elif dimension & (dimension - 1) == 0:
        dims = (2,) * (dimension.bit_length() - 1)
    else:
        dims = (dimension,)

    if int(np.prod(dims, dtype=int)) != dimension:
        raise ValueError("Subsystem dimensions do not match the state.")

    qargs_B = list(qargs_B)
    if (
        any(not isinstance(q, (int, np.integer)) for q in qargs_B)
        or len(set(qargs_B)) != len(qargs_B)
        or any(q < 0 or q >= len(dims) for q in qargs_B)
    ):
        raise ValueError("Invalid subsystem partition.")

    subsystem_B = sorted(qargs_B)
    subsystem_A = [q for q in range(len(dims)) if q not in subsystem_B]

    n_qubits = max(1, (dimension - 1).bit_length())
    initial_state = np.zeros(1 << n_qubits, dtype=complex)
    initial_state[:dimension] = state

    machine = pq.CPUQVM()
    machine.init_qvm()
    try:
        qubits = machine.qAlloc_many(n_qubits)
        machine.init_state(initial_state.tolist(), qubits)
        program = pq.QProg()
        program << pq.I(qubits[0])
        machine.directly_run(program)
        simulated_state = np.asarray(machine.get_qstate(), dtype=complex)[:dimension]
    finally:
        machine.finalize()

    axes = [
        len(dims) - 1 - q
        for q in subsystem_A[::-1] + subsystem_B[::-1]
    ]
    dim_A = int(np.prod([dims[q] for q in subsystem_A], dtype=int))
    dim_B = int(np.prod([dims[q] for q in subsystem_B], dtype=int))
    matrix = simulated_state.reshape(dims[::-1]).transpose(axes).reshape(dim_A, dim_B)
    left, coefficients, right = np.linalg.svd(matrix, full_matrices=False)

    return [
        (float(coefficient), left[:, i].copy(), right[i, :].copy())
        for i, coefficient in enumerate(coefficients)
        if coefficient > 1e-10
    ]
