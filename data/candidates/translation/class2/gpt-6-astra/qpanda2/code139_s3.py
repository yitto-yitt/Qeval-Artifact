# EVAL_META: task_id=139, framework=qpanda2, class=2
import numpy as np
import pyqpanda as pq


def schmidt_test(data, qargs_B):
    raw = data if isinstance(data, (list, tuple, np.ndarray)) else getattr(data, "data", data)
    array = np.asarray(raw, dtype=complex)

    if array.ndim == 1:
        vector = array.copy()
    elif array.ndim == 2 and array.shape[0] == array.shape[1]:
        if not np.allclose(array, array.conj().T, atol=1e-8, rtol=1e-5):
            raise ValueError("The density matrix must be Hermitian.")
        eigenvalues, eigenvectors = np.linalg.eigh(array)
        vector = eigenvectors[:, np.argmax(eigenvalues)]
        if not np.allclose(
            array, np.outer(vector, vector.conj()), atol=1e-8, rtol=1e-5
        ):
            raise ValueError("Schmidt decomposition requires a pure state.")
    else:
        raise ValueError("Expected a statevector or a square density matrix.")

    size = vector.size
    if size == 0 or not np.isclose(np.vdot(vector, vector), 1, atol=1e-8, rtol=1e-5):
        raise ValueError("The input state must be normalized.")

    dims_method = getattr(data, "dims", None)
    if callable(dims_method):
        dims = tuple(int(d) for d in dims_method())
    elif size > 1 and size & (size - 1) == 0:
        dims = (2,) * (size.bit_length() - 1)
    else:
        dims = (size,)

    if int(np.prod(dims)) != size:
        raise ValueError("Subsystem dimensions do not match the state.")

    subsystem_b = sorted(set(int(i) for i in qargs_B))
    if any(i < 0 or i >= len(dims) for i in subsystem_b):
        raise ValueError("Invalid subsystem index.")
    subsystem_a = [i for i in range(len(dims)) if i not in subsystem_b]

    machine = pq.CPUQVM()
    machine.init_qvm()
    try:
        qubit_count = max(1, (size - 1).bit_length())
        qubits = machine.qAlloc_many(qubit_count)
        initial_state = np.zeros(1 << qubit_count, dtype=complex)
        initial_state[:size] = vector
        machine.init_state(initial_state.tolist())

        program = pq.QProg()
        program << pq.I(qubits[0])
        machine.directly_run(program)
        state = np.asarray(machine.get_qstate(), dtype=complex)[:size].copy()
    finally:
        machine.finalize()

    axes = [
        len(dims) - 1 - i
        for i in subsystem_a[::-1] + subsystem_b[::-1]
    ]
    dimension_a = int(np.prod([dims[i] for i in subsystem_a], dtype=int))
    dimension_b = int(np.prod([dims[i] for i in subsystem_b], dtype=int))
    matrix = state.reshape(dims[::-1]).transpose(axes).reshape(
        dimension_a, dimension_b
    )

    vectors_a, coefficients, vectors_b = np.linalg.svd(matrix, full_matrices=False)
    return [
        (float(coefficient), vectors_a[:, i].copy(), vectors_b[i, :].copy())
        for i, coefficient in enumerate(coefficients)
        if coefficient > 1e-10
    ]
