# EVAL_META: task_id=139, framework=qpanda2, class=2
import numpy as np
import pyqpanda as pq


def schmidt_test(data, qargs_B):
    atol, rtol = 1e-8, 1e-5
    dims_method = getattr(data, "dims", None)
    dims = tuple(dims_method()) if callable(dims_method) else None
    raw = data.data if callable(dims_method) else data
    array = np.asarray(raw, dtype=complex)

    if array.ndim == 2 and array.shape[0] == array.shape[1]:
        if not np.allclose(array, array.conj().T, atol=atol, rtol=rtol):
            raise ValueError("The density matrix must be Hermitian.")
        eigenvalues, eigenvectors = np.linalg.eigh(array)
        vector = eigenvectors[:, np.argmax(eigenvalues)]
        if not np.allclose(
            array, np.outer(vector, vector.conj()), atol=atol, rtol=rtol
        ):
            raise ValueError("Schmidt decomposition requires a pure state.")
    elif array.ndim == 1:
        vector = array.copy()
    elif array.ndim == 2 and array.shape[1] == 1:
        vector = array[:, 0].copy()
    else:
        raise ValueError("Input must be a statevector or a pure density matrix.")

    size = vector.size
    if size == 0 or not np.isclose(
        np.vdot(vector, vector).real, 1.0, atol=atol, rtol=rtol
    ):
        raise ValueError("The input state is not normalized.")

    if dims is None:
        dims = (2,) * (size.bit_length() - 1) if size & (size - 1) == 0 else (size,)
    if int(np.prod(dims)) != size:
        raise ValueError("Subsystem dimensions do not match the state.")

    qargs_B = sorted(qargs_B)
    if len(set(qargs_B)) != len(qargs_B) or any(
        not isinstance(i, (int, np.integer)) or i < 0 or i >= len(dims)
        for i in qargs_B
    ):
        raise ValueError("Invalid subsystem partition.")
    qargs_A = [i for i in range(len(dims)) if i not in qargs_B]
    if not qargs_A:
        raise ValueError("Subsystem B must be a proper subset of the subsystems.")

    number_of_qubits = max(1, (size - 1).bit_length())
    padded = np.zeros(1 << number_of_qubits, dtype=complex)
    padded[:size] = vector

    machine = pq.CPUQVM()
    machine.init_qvm()
    try:
        qubits = machine.qAlloc_many(number_of_qubits)
        machine.init_state(padded.tolist(), qubits)
        program = pq.QProg()
        for qubit in qubits:
            program << pq.I(qubit)
        machine.directly_run(program)
        vector = np.asarray(machine.get_qstate(), dtype=complex)[:size]
    finally:
        machine.finalize()

    axes = [
        len(dims) - 1 - i
        for i in list(reversed(qargs_A)) + list(reversed(qargs_B))
    ]
    dimension_A = int(np.prod([dims[i] for i in qargs_A]))
    dimension_B = int(np.prod([dims[i] for i in qargs_B]))
    matrix = vector.reshape(dims[::-1]).transpose(axes).reshape(
        dimension_A, dimension_B
    )
    left, coefficients, right = np.linalg.svd(matrix, full_matrices=False)
    return [
        (float(coefficient), left[:, i].copy(), right[i, :].copy())
        for i, coefficient in enumerate(coefficients)
        if coefficient > atol
    ]
