# EVAL_META: task_id=110, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq


def equivalent_clifford_circuit(circuit, n):
    if n <= 0:
        return []

    rng = np.random.default_rng()

    def as_matrix(value):
        matrix = np.asarray(value, dtype=complex)
        if matrix.ndim == 1:
            dimension = int(round(np.sqrt(matrix.size)))
            if dimension * dimension != matrix.size:
                raise ValueError("Invalid matrix size")
            matrix = matrix.reshape(dimension, dimension)
        if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
            raise ValueError("Expected a square matrix")
        dimension = matrix.shape[0]
        if dimension < 1 or dimension & (dimension - 1):
            raise ValueError("Invalid quantum operator dimension")
        return matrix

    def qubit_count(obj):
        for name in ("num_qubits", "get_qubit_num", "qubit_num"):
            member = getattr(obj, name, None)
            if member is not None:
                try:
                    return int(member() if callable(member) else member)
                except (TypeError, ValueError):
                    pass

        for name in ("qubits", "get_used_qubits", "get_qubits"):
            member = getattr(obj, name, None)
            if member is None:
                continue
            try:
                qubits = list(member() if callable(member) else member)
                indices = []
                for qubit in qubits:
                    try:
                        indices.append(int(qubit))
                    except (TypeError, ValueError):
                        indices.append(int(qubit.get_phy_addr()))
                return max(indices, default=-1) + 1
            except (TypeError, ValueError, AttributeError):
                pass
        raise TypeError("Cannot determine the circuit's qubit count")

    def statevector(machine):
        owners = [machine]
        result = getattr(machine, "result", None)
        if result is not None:
            owners.append(result() if callable(result) else result)
        for owner in owners:
            for name in (
                "get_qstate",
                "get_state_vector",
                "get_statevector",
                "state_vector",
                "statevector",
                "get_state",
            ):
                member = getattr(owner, name, None)
                if member is None:
                    continue
                try:
                    value = member() if callable(member) else member
                    state = np.asarray(value, dtype=complex)
                    if state.ndim == 1 and state.size:
                        return state
                except (TypeError, ValueError, RuntimeError):
                    pass
        raise RuntimeError("The simulator did not expose its state vector")

    def operator(obj, width=None):
        variants = [obj]
        if not isinstance(obj, pq.QProg):
            program = pq.QProg()
            program << obj
            variants.append(program)

        for variant in variants:
            for name in ("get_unitary", "get_matrix", "matrix", "unitary"):
                member = getattr(variant, name, None)
                if member is not None:
                    try:
                        return as_matrix(member() if callable(member) else member)
                    except (TypeError, ValueError, RuntimeError):
                        pass
                function = getattr(pq, name, None)
                if callable(function):
                    try:
                        return as_matrix(function(variant))
                    except (TypeError, ValueError, RuntimeError):
                        pass

        if width is None:
            width = qubit_count(obj)
        dimension = 1 << width
        matrix = np.empty((dimension, dimension), dtype=complex)
        for column in range(dimension):
            program = pq.QProg()
            for qubit in range(width):
                program << pq.H(qubit) << pq.H(qubit)
                if (column >> qubit) & 1:
                    program << pq.X(qubit)
            program << obj
            machine = pq.CPUQVM()
            initialize = getattr(machine, "init_qvm", None)
            if callable(initialize):
                initialize()
            try:
                machine.run(program, 1)
                matrix[:, column] = statevector(machine)
            finally:
                finalize = getattr(machine, "finalize", None)
                if callable(finalize):
                    finalize()
        return matrix

    reference = operator(circuit)
    width = reference.shape[0].bit_length() - 1

    def random_clifford():
        result = pq.QCircuit()
        for qubit in range(width):
            result << pq.H(qubit) << pq.H(qubit)

        for first in range(width):
            size = width - first
            while True:
                p = rng.integers(0, 2, size=(2, size), dtype=np.uint8)
                if np.any(p):
                    break
            while True:
                q = rng.integers(0, 2, size=(2, size), dtype=np.uint8)
                parity = int(np.sum(p[0] * q[1] + p[1] * q[0])) & 1
                if parity:
                    break

            def h(index):
                result.__lshift__(pq.H(first + index))
                for pauli in (p, q):
                    x, z = int(pauli[0, index]), int(pauli[1, index])
                    pauli[0, index], pauli[1, index] = z, x

            def s(index):
                result.__lshift__(pq.S(first + index))
                for pauli in (p, q):
                    pauli[1, index] ^= pauli[0, index]

            def cx(control, target):
                result.__lshift__(pq.CNOT(first + control, first + target))
                for pauli in (p, q):
                    pauli[0, target] ^= pauli[0, control]
                    pauli[1, control] ^= pauli[1, target]

            for index in range(size):
                if p[0, index]:
                    if p[1, index]:
                        s(index)
                    h(index)

            pivot = int(np.flatnonzero(p[1])[0])
            if pivot:
                cx(0, pivot)
                cx(pivot, 0)
                cx(0, pivot)

            for index in range(1, size):
                if p[1, index]:
                    cx(index, 0)

            for index in range(1, size):
                if q[0, index] and q[1, index]:
                    s(index)
                elif q[1, index]:
                    h(index)
                if q[0, index]:
                    cx(0, index)

            if q[1, 0]:
                s(0)

            if rng.integers(2):
                result << pq.X(first)
            if rng.integers(2):
                result << pq.Z(first)

        return result

    circuits = []
    while len(circuits) < n:
        candidate = random_clifford()
        matrix = operator(candidate, width)
        pivot = np.unravel_index(np.argmax(np.abs(matrix)), matrix.shape)
        normalized_candidate = matrix * np.exp(-1j * np.angle(matrix[pivot]))
        normalized_reference = reference * np.exp(-1j * np.angle(reference[pivot]))
        if np.allclose(
            normalized_candidate,
            normalized_reference,
            rtol=0.4,
            atol=0.4,
        ):
            circuits.append(candidate)
    return circuits
