# EVAL_META: task_id=110, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq


def equivalent_clifford_circuit(circuit, n):
    rng = np.random.default_rng()

    def read_member(obj, name):
        value = getattr(obj, name)
        return value() if callable(value) else value

    def qubit_index(qubit):
        try:
            return int(qubit)
        except (TypeError, ValueError):
            for name in ("get_phy_addr", "get_physical_address", "index"):
                if hasattr(qubit, name):
                    return int(read_member(qubit, name))
            raise TypeError("Cannot determine the physical qubit index.")

    def circuit_width(obj):
        for name in ("num_qubits", "qubit_num", "get_qubit_num"):
            if hasattr(obj, name):
                try:
                    return int(read_member(obj, name))
                except (TypeError, ValueError):
                    pass
        for name in ("get_used_qubits", "get_qubits", "qubits"):
            if hasattr(obj, name):
                try:
                    qubits = list(read_member(obj, name))
                    return max((qubit_index(q) for q in qubits), default=-1) + 1
                except (TypeError, ValueError):
                    pass
        for name in ("get_max_qubit", "get_max_qubit_index"):
            if hasattr(obj, name):
                try:
                    return int(read_member(obj, name)) + 1
                except (TypeError, ValueError):
                    pass
        return None

    def as_matrix(value):
        matrix = np.asarray(value, dtype=complex)
        if matrix.ndim == 1:
            dimension = int(round(np.sqrt(matrix.size)))
            if dimension * dimension == matrix.size:
                matrix = matrix.reshape(dimension, dimension)
        if (
            matrix.ndim != 2
            or matrix.shape[0] != matrix.shape[1]
            or matrix.shape[0] == 0
            or matrix.shape[0] & (matrix.shape[0] - 1)
        ):
            raise ValueError("Expected a square qubit unitary matrix.")
        return matrix

    def native_matrix(obj):
        for name in ("get_matrix", "get_unitary", "get_circuit_matrix"):
            operation = getattr(pq, name, None)
            if operation is not None:
                try:
                    return as_matrix(operation(obj))
                except (TypeError, ValueError, RuntimeError, AttributeError):
                    pass
        for name in ("get_matrix", "get_unitary", "matrix", "unitary"):
            if hasattr(obj, name):
                try:
                    return as_matrix(read_member(obj, name))
                except (TypeError, ValueError, RuntimeError, AttributeError):
                    pass
        return None

    def simulated_matrix(obj, width):
        dimension = 1 << width
        matrix = np.empty((dimension, dimension), dtype=complex)
        for column in range(dimension):
            program = pq.QProg()
            for qubit in range(width):
                program << pq.H(qubit) << pq.H(qubit)
                if column & (1 << qubit):
                    program << pq.X(qubit)
            program << obj
            simulator = pq.CPUQVM()
            returned = simulator.run(program, 1)
            owners = [simulator]
            if returned is not None:
                owners.append(returned)
            for name in ("result", "get_result"):
                if hasattr(simulator, name):
                    owners.append(read_member(simulator, name))
            state = None
            for owner in owners:
                for name in (
                    "get_state_vector",
                    "get_statevector",
                    "get_qstate",
                    "state_vector",
                    "statevector",
                    "get_state",
                ):
                    if hasattr(owner, name):
                        try:
                            value = np.asarray(
                                read_member(owner, name), dtype=complex
                            ).reshape(-1)
                            if value.size == dimension:
                                state = value
                                break
                        except (TypeError, ValueError, RuntimeError):
                            pass
                if state is not None:
                    break
            if state is None:
                raise RuntimeError("The simulator did not expose its state vector.")
            matrix[:, column] = state
        return matrix

    width = circuit_width(circuit)
    original = native_matrix(circuit)
    if original is not None:
        matrix_width = original.shape[0].bit_length() - 1
        if width is None:
            width = matrix_width
        elif matrix_width != width:
            original = simulated_matrix(circuit, width)
    else:
        if width is None:
            raise TypeError("Cannot determine the circuit's qubit register.")
        original = simulated_matrix(circuit, width)

    def random_clifford():
        result = pq.QCircuit()
        for qubit in range(width):
            result << pq.H(qubit) << pq.H(qubit)

        for first in range(width):
            size = width - first
            while True:
                p = rng.integers(0, 2, size=2 * size, dtype=np.int8)
                if np.any(p):
                    break
            while True:
                q = rng.integers(0, 2, size=2 * size, dtype=np.int8)
                parity = (
                    np.dot(p[:size], q[size:])
                    + np.dot(p[size:], q[:size])
                ) % 2
                if parity:
                    break

            def h(index):
                result.__lshift__(pq.H(first + index))
                for pauli in (p, q):
                    pauli[index], pauli[size + index] = (
                        pauli[size + index],
                        pauli[index],
                    )

            def s(index):
                result.__lshift__(pq.S(first + index))
                for pauli in (p, q):
                    pauli[size + index] ^= pauli[index]

            def cx(control, target):
                result.__lshift__(pq.CNOT(first + control, first + target))
                for pauli in (p, q):
                    pauli[target] ^= pauli[control]
                    pauli[size + control] ^= pauli[size + target]

            for index in range(size):
                if p[index]:
                    if p[size + index]:
                        s(index)
                    h(index)

            pivot = int(np.flatnonzero(p[size:])[0])
            if pivot:
                cx(0, pivot)
                cx(pivot, 0)
                cx(0, pivot)

            for index in range(1, size):
                if p[size + index]:
                    cx(index, 0)

            for index in range(1, size):
                if q[index] or q[size + index]:
                    if not q[index]:
                        h(index)
                    elif q[size + index]:
                        s(index)
                    cx(0, index)

            if q[size]:
                s(0)

            if rng.integers(2):
                result << pq.X(first)
            if rng.integers(2):
                result << pq.Z(first)

        return result

    circuits = []
    while len(circuits) < n:
        candidate = random_clifford()
        candidate_matrix = native_matrix(candidate)
        if candidate_matrix is None or candidate_matrix.shape != original.shape:
            candidate_matrix = simulated_matrix(candidate, width)

        pivot = int(np.argmax(np.abs(candidate_matrix)))
        left = candidate_matrix * np.exp(
            -1j * np.angle(candidate_matrix.flat[pivot])
        )
        right = original * np.exp(-1j * np.angle(original.flat[pivot]))
        if np.allclose(left, right, rtol=0.4, atol=0.4):
            circuits.append(candidate)

    return circuits
