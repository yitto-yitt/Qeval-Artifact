# EVAL_META: task_id=139, framework=qpanda, class=2
import numpy as np
import pyqpanda3.core as pq


def schmidt_test(data, qargs_B):
    raw = data.data if hasattr(data, "dims") and hasattr(data, "data") else data
    array = np.asarray(raw, dtype=complex)

    if array.ndim == 1:
        state = array.copy()
        if not np.isclose(np.vdot(state, state), 1.0):
            raise ValueError("The statevector must be normalized.")
    elif array.ndim == 2 and array.shape[0] == array.shape[1]:
        if not np.allclose(array, array.conj().T):
            raise ValueError("The density matrix must be Hermitian.")
        values, vectors = np.linalg.eigh(array)
        if not (
            np.isclose(values[-1], 1.0)
            and np.allclose(values[:-1], 0.0)
        ):
            raise ValueError("Schmidt decomposition requires a pure state.")
        state = vectors[:, -1]
        nonzero = np.flatnonzero(np.abs(state) > 1e-8)
        if nonzero.size:
            state = state / (state[nonzero[0]] / abs(state[nonzero[0]]))
    else:
        raise ValueError("Expected a statevector or a square density matrix.")

    dimension = state.size
    if dimension == 0:
        raise ValueError("The state must not be empty.")

    if hasattr(data, "dims") and callable(data.dims):
        dims = tuple(data.dims())
    elif dimension & (dimension - 1) == 0:
        dims = (2,) * (dimension.bit_length() - 1)
    else:
        dims = (dimension,)

    subsystem_b = sorted(qargs_B)
    if (
        len(set(subsystem_b)) != len(subsystem_b)
        or any(i < 0 or i >= len(dims) for i in subsystem_b)
    ):
        raise ValueError("Invalid subsystem partition.")
    subsystem_a = [i for i in range(len(dims)) if i not in subsystem_b]

    nqubits = max(1, (dimension - 1).bit_length())
    padded_dimension = 1 << nqubits
    initial = np.zeros(padded_dimension, dtype=complex)
    initial[:dimension] = state
    initial /= np.linalg.norm(initial)

    columns = np.column_stack((initial, np.eye(padded_dimension, dtype=complex)))
    unitary, _ = np.linalg.qr(columns, mode="reduced")
    unitary[:, 0] = initial

    machine = pq.CPUQVM()
    if hasattr(machine, "init_qvm"):
        machine.init_qvm()
    if hasattr(machine, "qAlloc_many"):
        qubits = machine.qAlloc_many(nqubits)
    else:
        qubits = list(range(nqubits))

    program = pq.QProg()
    if hasattr(pq, "QOracle"):
        try:
            preparation = pq.QOracle(qubits, unitary.tolist())
        except TypeError:
            preparation = pq.QOracle(qubits, unitary.ravel().tolist())
    else:
        preparation = pq.matrix_decompose(qubits, unitary.tolist())
    program << preparation

    if hasattr(machine, "run"):
        try:
            run_result = machine.run(program, 1)
        except TypeError:
            run_result = machine.run(program)
    else:
        run_result = machine.directly_run(program)

    sources = [machine, run_result]
    if hasattr(machine, "result"):
        sources.insert(0, machine.result())

    simulated = None
    for source in sources:
        if source is None:
            continue
        for name in ("get_state_vector", "get_statevector", "get_qstate"):
            getter = getattr(source, name, None)
            if callable(getter):
                simulated = np.asarray(getter(), dtype=complex).reshape(-1)
                break
        if simulated is not None:
            break
    if simulated is None:
        raise RuntimeError("The simulator did not expose its statevector.")

    simulated = simulated[:dimension]
    overlap = np.vdot(state, simulated)
    if abs(overlap) > 0:
        simulated *= np.conj(overlap) / abs(overlap)
    simulated *= np.linalg.norm(state) / np.linalg.norm(simulated)

    axes = [
        len(dims) - 1 - i
        for i in list(reversed(subsystem_a)) + list(reversed(subsystem_b))
    ]
    dimension_a = int(np.prod([dims[i] for i in subsystem_a], dtype=int))
    dimension_b = int(np.prod([dims[i] for i in subsystem_b], dtype=int))
    bipartite = simulated.reshape(tuple(reversed(dims)))
    bipartite = bipartite.transpose(axes).reshape(dimension_a, dimension_b)
    vectors_a, coefficients, vectors_b = np.linalg.svd(
        bipartite, full_matrices=False
    )
    return [
        (float(coefficient), vectors_a[:, i].copy(), vectors_b[i, :].copy())
        for i, coefficient in enumerate(coefficients)
        if coefficient > 1e-12
    ]
