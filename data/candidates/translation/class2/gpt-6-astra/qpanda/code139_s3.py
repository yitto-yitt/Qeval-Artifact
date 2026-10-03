# EVAL_META: task_id=139, framework=qpanda, class=2
import numpy as np
from pyqpanda3.core import CPUQVM, QProg, RY, RZ, X


def schmidt_test(data, qargs_B):
    dims_method = getattr(data, "dims", None)
    dims = tuple(dims_method()) if callable(dims_method) else None
    raw = data if isinstance(data, (np.ndarray, list, tuple)) else getattr(data, "data", data)
    array = np.asarray(raw, dtype=complex)

    if array.ndim == 2:
        if array.shape[0] != array.shape[1]:
            raise ValueError("The density matrix must be square.")
        if not np.allclose(array, array.conj().T):
            raise ValueError("The density matrix must be Hermitian.")
        values, vectors = np.linalg.eigh(array)
        if not np.isclose(values[-1], 1.0) or not np.allclose(values[:-1], 0.0):
            raise ValueError("Schmidt decomposition requires a pure state.")
        state = vectors[:, -1]
    elif array.ndim == 1:
        state = array.copy()
    else:
        raise ValueError("Expected a statevector or a pure-state density matrix.")

    size = state.size
    if not size or not np.isclose(np.vdot(state, state).real, 1.0):
        raise ValueError("The state must be normalized.")

    if dims is None:
        dims = (2,) * (size.bit_length() - 1) if size & (size - 1) == 0 else (size,)
    if np.prod(dims, dtype=int) != size:
        raise ValueError("Invalid subsystem dimensions.")

    subsystem_B = sorted(int(q) for q in qargs_B)
    if len(set(subsystem_B)) != len(subsystem_B):
        raise ValueError("Subsystem indices must be distinct.")
    if any(q < 0 or q >= len(dims) for q in subsystem_B):
        raise ValueError("Invalid subsystem index.")
    subsystem_A = [q for q in range(len(dims)) if q not in subsystem_B]

    nqubits = max(1, (size - 1).bit_length())
    amplitudes = np.zeros(1 << nqubits, dtype=complex)
    amplitudes[:size] = state
    phases = np.angle(amplitudes)
    program = QProg()

    def append_conditioned(gate, controls, prefix):
        zero_controls = [
            q for bit, q in enumerate(controls) if not ((prefix >> bit) & 1)
        ]
        for q in zero_controls:
            program.__lshift__(X(q))
        if controls:
            controlled = gate.control(controls)
            if controlled is not None:
                gate = controlled
        program.__lshift__(gate)
        for q in reversed(zero_controls):
            program.__lshift__(X(q))

    for target in reversed(range(nqubits)):
        controls = list(range(target + 1, nqubits))
        half = 1 << target
        for prefix in range(1 << len(controls)):
            start = prefix << (target + 1)
            middle = start + half
            end = middle + half
            left = np.linalg.norm(amplitudes[start:middle])
            right = np.linalg.norm(amplitudes[middle:end])
            angle = 2.0 * np.arctan2(right, left)
            append_conditioned(RY(target, float(angle)), controls, prefix)

    for target in reversed(range(nqubits)):
        controls = list(range(target + 1, nqubits))
        half = 1 << target
        for prefix in range(1 << len(controls)):
            start = prefix << (target + 1)
            middle = start + half
            end = middle + half
            angle = phases[middle:end].mean() - phases[start:middle].mean()
            if angle != 0.0:
                append_conditioned(RZ(target, float(angle)), controls, prefix)

    simulator = CPUQVM()
    try:
        execution_result = simulator.run(program, 1)
    except TypeError:
        execution_result = simulator.run(program)

    sources = [simulator, execution_result]
    result_accessor = getattr(simulator, "result", None)
    if result_accessor is not None:
        sources.append(result_accessor() if callable(result_accessor) else result_accessor)

    simulated = None
    for source in sources:
        if source is None:
            continue
        for name in (
            "get_state_vector",
            "get_statevector",
            "get_qstate",
            "state_vector",
            "statevector",
            "get_state",
        ):
            accessor = getattr(source, name, None)
            if accessor is None:
                continue
            try:
                value = accessor() if callable(accessor) else accessor
            except TypeError:
                continue
            if isinstance(value, dict):
                candidate = np.zeros(1 << nqubits, dtype=complex)
                for key, amplitude in value.items():
                    index = int(key, 2) if isinstance(key, str) else int(key)
                    candidate[index] = amplitude
            else:
                try:
                    candidate = np.asarray(value, dtype=complex).reshape(-1)
                except (TypeError, ValueError):
                    continue
            if candidate.size == 1 << nqubits:
                simulated = candidate
                break
        if simulated is not None:
            break

    if simulated is None:
        raise RuntimeError("The simulator did not expose its statevector.")

    simulated = simulated[:size] * np.exp(1j * phases.mean())
    axes = [
        len(dims) - 1 - q
        for q in list(reversed(subsystem_A)) + list(reversed(subsystem_B))
    ]
    dimension_A = int(np.prod([dims[q] for q in subsystem_A], dtype=int))
    dimension_B = int(np.prod([dims[q] for q in subsystem_B], dtype=int))
    matrix = simulated.reshape(dims[::-1]).transpose(axes).reshape(
        dimension_A, dimension_B
    )
    vectors_A, coefficients, vectors_B = np.linalg.svd(matrix, full_matrices=False)
    return [
        (float(coefficient), vectors_A[:, i].copy(), vectors_B[i, :].copy())
        for i, coefficient in enumerate(coefficients)
        if not np.isclose(coefficient, 0.0)
    ]
