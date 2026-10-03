# EVAL_META: task_id=110, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq


def equivalent_clifford_circuit(circuit, n):
    rng = np.random.default_rng()

    def as_program(obj):
        if isinstance(obj, pq.QProg):
            return obj
        prog = pq.QProg()
        prog << obj
        return prog

    def state_vector(prog):
        simulator = pq.CPUQVM()
        try:
            result = simulator.run(prog, 1)
        except TypeError:
            result = simulator.run(prog)

        sources = [simulator, result]
        result_method = getattr(simulator, "result", None)
        if callable(result_method):
            sources.append(result_method())

        for source in sources:
            if source is None:
                continue
            for name in (
                "get_state_vector",
                "get_qstate",
                "get_statevector",
                "state_vector",
            ):
                getter = getattr(source, name, None)
                if getter is None:
                    continue
                try:
                    value = getter() if callable(getter) else getter
                    state = np.asarray(value, dtype=complex).reshape(-1)
                except (TypeError, ValueError, RuntimeError):
                    continue
                size = state.size
                if size and size & (size - 1) == 0:
                    return state
        raise RuntimeError("The simulator did not expose its state vector.")

    def operator_matrix(obj, width=None):
        prog = as_program(obj)
        for owner, names, arguments in (
            (obj, ("get_unitary", "get_matrix", "matrix"), ()),
            (pq, ("get_unitary", "get_matrix"), (prog,)),
        ):
            for name in names:
                getter = getattr(owner, name, None)
                if getter is None:
                    continue
                try:
                    value = getter(*arguments) if callable(getter) else getter
                    matrix = np.asarray(value, dtype=complex)
                    if matrix.ndim == 1:
                        dim = int(round(np.sqrt(matrix.size)))
                        if dim * dim != matrix.size:
                            continue
                        matrix = matrix.reshape(dim, dim)
                    if (
                        matrix.ndim == 2
                        and matrix.shape[0] == matrix.shape[1]
                        and matrix.shape[0] > 0
                        and matrix.shape[0] & (matrix.shape[0] - 1) == 0
                        and (
                            width is None
                            or matrix.shape[0] == 1 << width
                        )
                    ):
                        return matrix
                except (TypeError, ValueError, RuntimeError):
                    continue

        if width is None:
            first_column = state_vector(prog)
            width = first_column.size.bit_length() - 1
        else:
            first_column = None

        dim = 1 << width
        matrix = np.empty((dim, dim), dtype=complex)
        for basis in range(dim):
            if basis == 0 and first_column is not None:
                matrix[:, basis] = first_column
                continue
            experiment = pq.QProg()
            if width:
                experiment << pq.H(width - 1) << pq.H(width - 1)
            for qubit in range(width):
                if (basis >> qubit) & 1:
                    experiment << pq.X(qubit)
            experiment << prog
            matrix[:, basis] = state_vector(experiment)
        return matrix

    original = operator_matrix(circuit)
    num_qubits = original.shape[0].bit_length() - 1

    def random_clifford():
        prog = pq.QProg()

        for first in range(num_qubits):
            size = num_qubits - first

            while True:
                p = rng.integers(0, 2, size=(2, size), dtype=np.uint8)
                if np.any(p):
                    break

            while True:
                q = rng.integers(0, 2, size=(2, size), dtype=np.uint8)
                parity = (
                    int(np.dot(p[0], q[1]))
                    + int(np.dot(p[1], q[0]))
                ) & 1
                if parity:
                    break

            paulis = np.stack((p, q))

            def h(target):
                prog << pq.H(first + target)
                old_x = paulis[:, 0, target].copy()
                paulis[:, 0, target] = paulis[:, 1, target]
                paulis[:, 1, target] = old_x

            def s(target):
                prog << pq.S(first + target)
                paulis[:, 1, target] ^= paulis[:, 0, target]

            def cx(control, target):
                prog << pq.CNOT(first + control, first + target)
                paulis[:, 0, target] ^= paulis[:, 0, control]
                paulis[:, 1, control] ^= paulis[:, 1, target]

            for target in range(size):
                if paulis[0, 0, target]:
                    if paulis[0, 1, target]:
                        s(target)
                    h(target)

            pivot = int(np.flatnonzero(paulis[0, 1])[0])
            if pivot:
                cx(0, pivot)
                cx(pivot, 0)
                cx(0, pivot)

            for target in range(1, size):
                if paulis[0, 1, target]:
                    cx(target, 0)

            for target in range(1, size):
                x = int(paulis[1, 0, target])
                z = int(paulis[1, 1, target])
                if not (x or z):
                    continue
                if not x:
                    h(target)
                elif z:
                    s(target)
                cx(0, target)

            if paulis[1, 1, 0]:
                s(0)

            if rng.integers(2):
                prog << pq.X(first)
            if rng.integers(2):
                prog << pq.Z(first)

        if num_qubits:
            prog << pq.H(num_qubits - 1) << pq.H(num_qubits - 1)
        return prog

    circuits = []
    while len(circuits) < n:
        candidate = random_clifford()
        matrix = operator_matrix(candidate, num_qubits)
        pivot = int(np.argmax(np.abs(matrix)))
        candidate_phase = np.angle(matrix.flat[pivot])
        original_phase = np.angle(original.flat[pivot])

        if np.allclose(
            np.exp(-1j * candidate_phase) * matrix,
            np.exp(-1j * original_phase) * original,
            rtol=0.4,
            atol=0.4,
        ):
            circuits.append(candidate)

    return circuits
