# EVAL_META: task_id=139, framework=qpanda, class=2
import numpy as np
from pyqpanda3.core import CPUQVM, QProg, RY, RZ, X


def schmidt_test(data, qargs_B):
    dims_method = getattr(data, "dims", None)
    dims = tuple(dims_method()) if callable(dims_method) else None
    raw = data.data if callable(dims_method) else data
    state = np.asarray(raw, dtype=complex)

    if state.ndim == 2 and state.shape[1] == 1:
        state = state[:, 0]
    elif state.ndim == 2:
        if state.shape[0] != state.shape[1]:
            raise ValueError("The density matrix must be square.")
        if not np.allclose(state, state.conj().T, atol=1e-8, rtol=1e-5):
            raise ValueError("The density matrix must be Hermitian.")
        values, vectors = np.linalg.eigh(state)
        if not (
            np.isclose(values[-1], 1, atol=1e-8, rtol=1e-5)
            and np.allclose(values[:-1], 0, atol=1e-8, rtol=1e-5)
        ):
            raise ValueError("Schmidt decomposition requires a pure state.")
        state = vectors[:, -1].copy()
        nonzero = np.flatnonzero(np.abs(state) > 1e-8)
        if nonzero.size:
            first = state[nonzero[0]]
            state *= np.conj(first) / abs(first)
    elif state.ndim != 1:
        raise ValueError("Expected a statevector or density matrix.")

    dimension = state.size
    if dimension == 0 or not np.isclose(
        np.vdot(state, state).real, 1, atol=1e-8, rtol=1e-5
    ):
        raise ValueError("The state must be normalized.")

    if dims is None:
        if dimension & (dimension - 1) == 0:
            dims = (2,) * (dimension.bit_length() - 1)
        else:
            dims = (dimension,)
    if int(np.prod(dims)) != dimension:
        raise ValueError("Subsystem dimensions do not match the state.")

    subsystem_count = len(dims)
    qargs_B = sorted(qargs_B)
    if (
        not qargs_B
        or len(set(qargs_B)) != len(qargs_B)
        or any(q < 0 or q >= subsystem_count for q in qargs_B)
        or len(qargs_B) == subsystem_count
    ):
        raise ValueError("qargs_B must be a nonempty proper subsystem subset.")
    qargs_A = [q for q in range(subsystem_count) if q not in qargs_B]

    qubit_count = max(1, (dimension - 1).bit_length())
    amplitudes = np.zeros(1 << qubit_count, dtype=complex)
    amplitudes[:dimension] = state
    phases = np.angle(amplitudes)
    program = QProg()

    def append_conditioned(gate, target, prefix):
        controls = list(range(target + 1, qubit_count))
        zeros = [
            q for q in controls
            if not ((prefix >> (q - target - 1)) & 1)
        ]
        for q in zeros:
            program.__lshift__(X(q))
        if controls:
            gate = gate.control(controls)
        program.__lshift__(gate)
        for q in reversed(zeros):
            program.__lshift__(X(q))

    for target in range(qubit_count - 1, -1, -1):
        half = 1 << target
        width = half << 1
        for prefix in range(1 << (qubit_count - target - 1)):
            start = prefix * width
            lower = np.linalg.norm(amplitudes[start:start + half])
            upper = np.linalg.norm(amplitudes[start + half:start + width])
            angle = 2 * np.arctan2(upper, lower)
            append_conditioned(RY(target, float(angle)), target, prefix)

    for target in range(qubit_count - 1, -1, -1):
        half = 1 << target
        width = half << 1
        for prefix in range(1 << (qubit_count - target - 1)):
            start = prefix * width
            angle = (
                np.mean(phases[start + half:start + width])
                - np.mean(phases[start:start + half])
            )
            append_conditioned(RZ(target, float(angle)), target, prefix)

    simulator = CPUQVM()
    run_result = simulator.run(program, 1)
    result_accessor = getattr(simulator, "result", None)
    result = result_accessor() if callable(result_accessor) else result_accessor
    simulated = None
    for owner in (result, simulator, run_result):
        if owner is None:
            continue
        for name in (
            "get_state_vector",
            "get_statevector",
            "get_qstate",
            "state_vector",
            "statevector",
        ):
            accessor = getattr(owner, name, None)
            if accessor is None:
                continue
            value = accessor() if callable(accessor) else accessor
            if isinstance(value, dict):
                candidate = np.zeros(1 << qubit_count, dtype=complex)
                for key, amplitude in value.items():
                    index = int(key, 2) if isinstance(key, str) else int(key)
                    candidate[index] = amplitude
            else:
                candidate = np.asarray(value, dtype=complex).reshape(-1)
            if candidate.size == 1 << qubit_count:
                simulated = candidate
                break
        if simulated is not None:
            break
    if simulated is None:
        raise RuntimeError("The simulator did not expose its statevector.")

    simulated = simulated[:dimension] * np.exp(1j * np.mean(phases))
    simulated *= np.linalg.norm(state)
    axes = [
        subsystem_count - 1 - q
        for q in reversed(qargs_A)
    ] + [
        subsystem_count - 1 - q
        for q in reversed(qargs_B)
    ]
    dim_A = int(np.prod([dims[q] for q in qargs_A]))
    dim_B = int(np.prod([dims[q] for q in qargs_B]))
    matrix = simulated.reshape(dims[::-1]).transpose(axes).reshape(dim_A, dim_B)
    left, coefficients, right = np.linalg.svd(matrix, full_matrices=False)
    return [
        (float(coefficient), left[:, i].copy(), right[i, :].copy())
        for i, coefficient in enumerate(coefficients)
        if coefficient > 1e-12
    ]
