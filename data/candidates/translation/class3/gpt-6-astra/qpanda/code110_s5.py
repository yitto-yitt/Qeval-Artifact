# EVAL_META: task_id=110, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq


def equivalent_clifford_circuit(circuit, n):
    rng = np.random.default_rng()

    def as_program(obj):
        program = pq.QProg()
        program << obj
        return program

    def qubit_count(obj):
        for name in (
            "num_qubits", "get_qubit_num", "get_qubits_num",
            "qubit_num", "get_used_qubit_num",
        ):
            try:
                value = getattr(obj, name)
                value = value() if callable(value) else value
                return int(value)
            except (AttributeError, TypeError, ValueError):
                pass
        for name in ("get_max_qubit_index", "get_max_qubit_addr"):
            try:
                return int(getattr(obj, name)()) + 1
            except (AttributeError, TypeError, ValueError):
                pass
        for name in ("get_used_qubits", "get_qubits", "qubits"):
            try:
                value = getattr(obj, name)
                qubits = list(value() if callable(value) else value)
                indices = []
                for qubit in qubits:
                    try:
                        indices.append(int(qubit))
                    except (TypeError, ValueError):
                        indices.append(int(qubit.get_phy_addr()))
                return max(indices, default=-1) + 1
            except (AttributeError, TypeError, ValueError):
                pass
        return None

    def square_matrix(value, width=None):
        array = np.asarray(value, dtype=complex)
        if array.ndim == 1:
            dimension = int(round(np.sqrt(array.size)))
            if dimension * dimension != array.size:
                raise ValueError("Not a square matrix")
            array = array.reshape(dimension, dimension)
        if array.ndim != 2 or array.shape[0] != array.shape[1]:
            raise ValueError("Not a square matrix")
        dimension = array.shape[0]
        if dimension == 0 or dimension & (dimension - 1):
            raise ValueError("Not a qubit operator")
        if width is not None and dimension != 1 << width:
            raise ValueError("Incorrect operator dimension")
        return array

    def framework_matrix(obj, width=None):
        program = as_program(obj)
        objects = (obj, program)
        preferred = (
            "get_matrix", "matrix", "get_unitary", "unitary",
            "get_qprog_matrix", "get_circuit_matrix", "get_unitary_matrix",
        )
        for owner in (*objects, pq):
            names = list(preferred)
            names.extend(
                name for name in dir(owner)
                if not name.startswith("_")
                and ("matrix" in name.lower() or "unitary" in name.lower())
                and name not in names
            )
            for name in names:
                try:
                    accessor = getattr(owner, name)
                except AttributeError:
                    continue
                arguments = [(candidate,) for candidate in objects] if owner is pq else [()]
                if width is not None:
                    arguments += (
                        [(candidate, width) for candidate in objects]
                        if owner is pq else [(width,)]
                    )
                for args in arguments:
                    try:
                        value = accessor(*args) if callable(accessor) else accessor
                        return square_matrix(value, width)
                    except Exception:
                        continue

        if width is None:
            width = qubit_count(obj)
        if width is None:
            width = qubit_count(program)
        if width is None:
            raise TypeError("Cannot determine the quantum program's qubit count")

        machine = pq.CPUQVM()
        for name in ("init_qvm", "init"):
            initializer = getattr(machine, name, None)
            if callable(initializer):
                initializer()
                break

        columns = []
        for basis in range(1 << width):
            prepared = pq.QProg()
            for qubit in range(width):
                prepared << pq.H(qubit) << pq.H(qubit)
                if basis & (1 << qubit):
                    prepared << pq.X(qubit)
            prepared << obj
            try:
                returned = machine.run(prepared, 1)
            except TypeError:
                returned = machine.run(prepared)

            sources = [machine, returned]
            for name in ("result", "get_result"):
                try:
                    result = getattr(machine, name)
                    sources.append(result() if callable(result) else result)
                except (AttributeError, TypeError):
                    pass

            state = None
            for source in sources:
                if source is None:
                    continue
                names = [
                    "get_qstate", "get_state_vector", "get_statevector",
                    "get_quantum_state", "get_state", "state_vector",
                    "statevector", "state",
                ]
                names.extend(
                    name for name in dir(source)
                    if "state" in name.lower() and not name.startswith("_")
                    and name not in names
                )
                for name in names:
                    try:
                        accessor = getattr(source, name)
                        value = accessor() if callable(accessor) else accessor
                        candidate = np.asarray(value, dtype=complex).reshape(-1)
                        if candidate.size == 1 << width:
                            state = candidate
                            break
                    except Exception:
                        continue
                if state is not None:
                    break
            if state is None:
                raise RuntimeError("The simulator did not expose its state vector")
            columns.append(state)
        return np.column_stack(columns)

    original = framework_matrix(circuit)
    num_qubits = original.shape[0].bit_length() - 1

    def random_clifford():
        reductions = []

        for first in range(num_qubits):
            size = num_qubits - first
            while True:
                p = rng.integers(0, 2, size=(2, size), dtype=np.int8)
                if np.any(p):
                    break
            while True:
                q = rng.integers(0, 2, size=(2, size), dtype=np.int8)
                parity = (
                    np.dot(p[0].astype(np.int64), q[1])
                    + np.dot(p[1].astype(np.int64), q[0])
                ) % 2
                if parity:
                    break

            def apply(kind, a, b=None):
                reductions.append(
                    (kind, first + a, None if b is None else first + b)
                )
                for pauli in (p, q):
                    x, z = pauli
                    if kind == "h":
                        x[a], z[a] = int(z[a]), int(x[a])
                    elif kind == "s":
                        z[a] ^= x[a]
                    else:
                        x[b] ^= x[a]
                        z[a] ^= z[b]

            for j in range(size):
                if p[0, j]:
                    if p[1, j]:
                        apply("s", j)
                    apply("h", j)

            pivot = int(np.flatnonzero(p[1])[0])
            if pivot:
                apply("cx", 0, pivot)
                apply("cx", pivot, 0)
                apply("cx", 0, pivot)

            for j in range(1, size):
                if p[1, j]:
                    apply("cx", j, 0)

            for j in range(1, size):
                if q[0, j]:
                    apply("cx", 0, j)
                if q[1, j]:
                    apply("h", j)
                    apply("cx", 0, j)
                    apply("h", j)
            if q[1, 0]:
                apply("s", 0)

        candidate = pq.QCircuit()
        for qubit in range(num_qubits):
            candidate << pq.H(qubit) << pq.H(qubit)

        for kind, a, b in reversed(reductions):
            if kind == "h":
                candidate << pq.H(a)
            elif kind == "s":
                candidate << pq.S(a) << pq.S(a) << pq.S(a)
            else:
                candidate << pq.CNOT(a, b)

        for qubit in range(num_qubits):
            if rng.integers(2):
                candidate << pq.X(qubit)
            if rng.integers(2):
                candidate << pq.Z(qubit)
        return candidate

    circuits = []
    pivot = np.unravel_index(np.argmax(np.abs(original)), original.shape)
    while len(circuits) < n:
        candidate = random_clifford()
        operator = framework_matrix(candidate, num_qubits)
        if abs(operator[pivot]) > 0:
            phase = operator[pivot] / original[pivot]
            phase /= abs(phase)
            if np.allclose(operator, phase * original, rtol=0.4, atol=0.4):
                circuits.append(candidate)
    return circuits
