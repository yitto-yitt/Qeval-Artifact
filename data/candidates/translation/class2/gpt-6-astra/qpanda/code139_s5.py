# EVAL_META: task_id=139, framework=qpanda, class=2
import numpy as np
from pyqpanda3 import core


def schmidt_test(data, qargs_B):
    dims_method = getattr(data, "dims", None)
    dims = tuple(dims_method()) if callable(dims_method) else None
    raw = data
    if not isinstance(data, (np.ndarray, list, tuple)) and hasattr(data, "data"):
        raw = data.data
    array = np.asarray(raw, dtype=complex)

    if array.ndim == 1:
        vector = array.copy()
    elif array.ndim == 2 and array.shape[0] == array.shape[1]:
        if not np.allclose(array, array.conj().T):
            raise ValueError("The density matrix must be Hermitian.")
        values, vectors = np.linalg.eigh(array)
        index = int(np.argmax(values))
        expected = np.zeros_like(values)
        expected[index] = 1.0
        if not np.allclose(values, expected):
            raise ValueError("Schmidt decomposition requires a pure state.")
        vector = vectors[:, index]
        nonzero = np.flatnonzero(np.abs(vector) > 1e-12)
        if nonzero.size:
            vector = vector * np.exp(-1j * np.angle(vector[nonzero[0]]))
    else:
        raise ValueError("Expected a statevector or a pure-state density matrix.")

    dimension = vector.size
    if dimension == 0 or not np.isclose(np.vdot(vector, vector), 1.0):
        raise ValueError("The state must be normalized.")

    if dims is None:
        if dimension & (dimension - 1) == 0:
            dims = (2,) * (dimension.bit_length() - 1)
        else:
            dims = (dimension,)
    if int(np.prod(dims)) != dimension:
        raise ValueError("Subsystem dimensions do not match the state.")

    subsystem_B = sorted(int(q) for q in qargs_B)
    if len(set(subsystem_B)) != len(subsystem_B):
        raise ValueError("Subsystem indices must be distinct.")
    if any(q < 0 or q >= len(dims) for q in subsystem_B):
        raise ValueError("Invalid subsystem index.")
    subsystem_A = [q for q in range(len(dims)) if q not in subsystem_B]

    nqubits = max(1, (dimension - 1).bit_length())
    padded = np.zeros(1 << nqubits, dtype=complex)
    padded[:dimension] = vector
    magnitudes = np.abs(padded)
    phases = np.angle(padded)
    program = core.QProg()

    def multiplexed_rotation(gate, target, angles):
        angles = np.asarray(angles, dtype=float)
        count = angles.size
        coefficients = angles.copy()
        stride = 1
        while stride < count:
            for start in range(0, count, 2 * stride):
                left = coefficients[start:start + stride].copy()
                right = coefficients[start + stride:start + 2 * stride].copy()
                coefficients[start:start + stride] = left + right
                coefficients[start + stride:start + 2 * stride] = left - right
            stride *= 2
        coefficients /= count
        for index in range(count):
            gray = index ^ (index >> 1)
            program.__lshift__(gate(target, float(coefficients[gray])))
            if count > 1:
                following = (index + 1) % count
                next_gray = following ^ (following >> 1)
                changed_bit = (gray ^ next_gray).bit_length() - 1
                program.__lshift__(core.CNOT(target + 1 + changed_bit, target))

    for target in range(nqubits - 1, -1, -1):
        half = 1 << target
        block = half << 1
        angles = []
        for start in range(0, padded.size, block):
            left = np.linalg.norm(magnitudes[start:start + half])
            right = np.linalg.norm(magnitudes[start + half:start + block])
            angles.append(2.0 * np.arctan2(right, left))
        multiplexed_rotation(core.RY, target, angles)

    for target in range(nqubits - 1, -1, -1):
        half = 1 << target
        block = half << 1
        angles = [
            np.mean(phases[start + half:start + block])
            - np.mean(phases[start:start + half])
            for start in range(0, padded.size, block)
        ]
        multiplexed_rotation(core.RZ, target, angles)

    simulator = core.CPUQVM()
    run_result = simulator.run(program)
    holders = [simulator, run_result]
    for name in ("result", "get_result"):
        accessor = getattr(simulator, name, None)
        if accessor is not None:
            holders.append(accessor() if callable(accessor) else accessor)

    simulated = None
    for holder in holders:
        if holder is None:
            continue
        for name in (
            "get_state_vector",
            "get_statevector",
            "get_qstate",
            "state_vector",
            "statevector",
            "get_state",
        ):
            accessor = getattr(holder, name, None)
            if accessor is None:
                continue
            candidate = accessor() if callable(accessor) else accessor
            if isinstance(candidate, dict):
                state = np.zeros(padded.size, dtype=complex)
                for key, value in candidate.items():
                    position = int(key, 2) if isinstance(key, str) else int(key)
                    state[position] = value
            else:
                state = np.asarray(candidate, dtype=complex).reshape(-1)
            if state.size == padded.size:
                simulated = state
                break
        if simulated is not None:
            break

    if simulated is None:
        raise RuntimeError("The simulator did not expose its final statevector.")

    simulated = simulated[:dimension] * np.exp(1j * np.mean(phases))
    tensor = simulated.reshape(tuple(reversed(dims)))
    axes = [
        len(dims) - 1 - q
        for q in list(reversed(subsystem_A)) + list(reversed(subsystem_B))
    ]
    size_A = int(np.prod([dims[q] for q in subsystem_A], dtype=int))
    size_B = int(np.prod([dims[q] for q in subsystem_B], dtype=int))
    matrix = tensor.transpose(axes).reshape(size_A, size_B)
    left, coefficients, right = np.linalg.svd(matrix, full_matrices=False)

    return [
        (float(coefficient), left[:, index].copy(), right[index, :].copy())
        for index, coefficient in enumerate(coefficients)
        if not np.isclose(coefficient, 0.0)
    ]
