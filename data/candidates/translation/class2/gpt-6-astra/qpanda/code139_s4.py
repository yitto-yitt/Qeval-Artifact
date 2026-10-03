# EVAL_META: task_id=139, framework=qpanda, class=2
import numpy as np
from pyqpanda3.core import CPUQVM, QProg, RY, RZ, X


def schmidt_test(data, qargs_B):
    dims_method = getattr(data, "dims", None)
    dims = tuple(dims_method()) if callable(dims_method) else None
    raw = data if isinstance(data, (list, tuple, np.ndarray)) else getattr(data, "data", data)
    state = np.asarray(raw, dtype=complex)

    if state.ndim == 2:
        if state.shape[0] != state.shape[1]:
            raise ValueError("The density matrix must be square.")
        if not np.allclose(state, state.conj().T):
            raise ValueError("The density matrix must be Hermitian.")
        eigenvalues, eigenvectors = np.linalg.eig(state)
        index = int(np.argmax(eigenvalues.real))
        remaining = np.delete(eigenvalues, index)
        if not np.isclose(eigenvalues[index], 1.0) or not np.allclose(remaining, 0.0):
            raise ValueError("Schmidt decomposition requires a pure state.")
        state = eigenvectors[:, index]
    elif state.ndim != 1:
        raise ValueError("Expected a statevector or a density matrix.")

    size = state.size
    if size == 0 or not np.isclose(np.vdot(state, state).real, 1.0):
        raise ValueError("The state must be normalized.")

    if dims is None:
        dims = (2,) * (size.bit_length() - 1) if size & (size - 1) == 0 else (size,)
    if np.prod(dims, dtype=int) != size:
        raise ValueError("Subsystem dimensions do not match the state.")

    subsystem_b = sorted(int(q) for q in qargs_B)
    if len(set(subsystem_b)) != len(subsystem_b):
        raise ValueError("Subsystem indices must be distinct.")
    if any(q < 0 or q >= len(dims) for q in subsystem_b):
        raise ValueError("Invalid subsystem index.")
    subsystem_a = [q for q in range(len(dims)) if q not in subsystem_b]
    if not subsystem_a or not subsystem_b:
        raise ValueError("Both parts of the partition must be nonempty.")

    num_qubits = max(1, (size - 1).bit_length())
    amplitudes = np.zeros(1 << num_qubits, dtype=complex)
    amplitudes[:size] = state
    phases = np.angle(amplitudes)
    program = QProg()

    for target in range(num_qubits - 1, -1, -1):
        controls = list(range(target + 1, num_qubits))
        block_size = 1 << (target + 1)
        half_size = 1 << target

        for prefix in range(1 << (num_qubits - target - 1)):
            start = prefix * block_size
            middle = start + half_size
            end = start + block_size

            left_norm = np.linalg.norm(amplitudes[start:middle])
            right_norm = np.linalg.norm(amplitudes[middle:end])
            theta = 2.0 * np.arctan2(right_norm, left_norm)
            phi = float(phases[middle:end].mean() - phases[start:middle].mean())

            negative_controls = [
                q for q in controls
                if not ((prefix >> (q - target - 1)) & 1)
            ]
            for q in negative_controls:
                program << X(q)

            rotation_y = RY(target, float(theta))
            rotation_z = RZ(target, phi)
            if controls:
                rotation_y = rotation_y.control(controls)
                rotation_z = rotation_z.control(controls)
            program << rotation_y
            program << rotation_z

            for q in reversed(negative_controls):
                program << X(q)

    simulator = CPUQVM()
    run_result = simulator.run(program, 1)
    result_method = getattr(simulator, "result", None)
    result = result_method() if callable(result_method) else run_result

    simulated = None
    for source in (result, simulator, run_result):
        if source is None:
            continue
        for name in ("get_state_vector", "get_qstate", "state_vector"):
            accessor = getattr(source, name, None)
            if accessor is not None:
                simulated = accessor() if callable(accessor) else accessor
                break
        if simulated is not None:
            break
    if simulated is None:
        raise RuntimeError("The simulator did not expose its statevector.")

    state = np.asarray(simulated, dtype=complex).reshape(-1)[:size]
    state = state * np.exp(1j * phases.mean())

    axes = [
        len(dims) - 1 - q
        for q in reversed(subsystem_a)
    ] + [
        len(dims) - 1 - q
        for q in reversed(subsystem_b)
    ]
    dimension_a = int(np.prod([dims[q] for q in subsystem_a]))
    dimension_b = int(np.prod([dims[q] for q in subsystem_b]))
    matrix = state.reshape(tuple(reversed(dims))).transpose(axes)
    matrix = matrix.reshape(dimension_a, dimension_b)

    vectors_a, coefficients, vectors_b = np.linalg.svd(matrix, full_matrices=False)
    return [
        (float(coefficient), vectors_a[:, i].copy(), vectors_b[i, :].copy())
        for i, coefficient in enumerate(coefficients)
        if coefficient > 1e-12
    ]
