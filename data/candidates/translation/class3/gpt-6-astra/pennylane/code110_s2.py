# EVAL_META: task_id=110, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def equivalent_clifford_circuit(circuit, n):
    if isinstance(circuit, qml.tape.QuantumScript):
        tape = circuit
    elif isinstance(circuit, qml.QNode):
        tape = circuit.construct((), {})
    elif callable(circuit):
        tape = qml.tape.make_qscript(circuit)()
    else:
        tape = qml.tape.QuantumScript(list(circuit))

    wires = list(tape.wires)
    num_qubits = len(wires)
    unitary_tape = qml.tape.QuantumScript(tape.operations)
    original = np.asarray(
        qml.matrix(unitary_tape, wire_order=wires), dtype=complex
    )
    rng = np.random.default_rng()
    results = []

    if num_qubits == 0:
        while len(results) < n:
            results.append(qml.tape.QuantumScript([]))
        return results

    dimension = 1 << num_qubits
    identity = np.eye(2, dtype=complex)
    pauli_x = np.array([[0, 1], [1, 0]], dtype=complex)
    pauli_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    pauli_z = np.array([[1, 0], [0, -1]], dtype=complex)

    def symplectic_product(a, b):
        return int(
            (
                np.dot(a[:num_qubits], b[num_qubits:])
                + np.dot(a[num_qubits:], b[:num_qubits])
            )
            % 2
        )

    def random_combination(basis):
        coefficients = rng.integers(0, 2, size=len(basis), dtype=np.int64)
        return (coefficients @ basis) % 2

    def independent_rows(rows):
        pivots = {}
        independent = []
        for row in rows:
            reduced = row.copy()
            for pivot in sorted(pivots):
                if reduced[pivot]:
                    reduced ^= pivots[pivot]
            nonzero = np.flatnonzero(reduced)
            if nonzero.size:
                pivots[int(nonzero[0])] = reduced
                independent.append(row.copy())
        return np.asarray(independent, dtype=np.int64).reshape(
            -1, 2 * num_qubits
        )

    def pauli_matrix(vector):
        matrix = np.ones((1, 1), dtype=complex)
        for wire in range(num_qubits):
            x = vector[wire]
            z = vector[num_qubits + wire]
            local = pauli_y if x and z else pauli_x if x else pauli_z if z else identity
            matrix = np.kron(matrix, local)
        return matrix if rng.integers(0, 2) == 0 else -matrix

    def random_clifford_matrix():
        basis = np.eye(2 * num_qubits, dtype=np.int64)
        z_generators = []
        x_generators = []

        for _ in range(num_qubits):
            z = random_combination(basis)
            while not np.any(z):
                z = random_combination(basis)

            x = random_combination(basis)
            while symplectic_product(z, x) != 1:
                x = random_combination(basis)

            z_generators.append(pauli_matrix(z))
            x_generators.append(pauli_matrix(x))

            projected = []
            for vector in basis:
                projected.append(
                    vector
                    ^ (symplectic_product(vector, x) * z)
                    ^ (symplectic_product(vector, z) * x)
                )
            basis = independent_rows(projected)

        state = rng.normal(size=dimension) + 1j * rng.normal(size=dimension)
        for generator in z_generators:
            state = (state + generator @ state) / 2
        state /= np.linalg.norm(state)

        matrix = np.empty((dimension, dimension), dtype=complex)
        matrix[:, 0] = state
        for column in range(1, dimension):
            bit = column & -column
            wire = num_qubits - bit.bit_length()
            matrix[:, column] = x_generators[wire] @ matrix[:, column ^ bit]
        return matrix

    while len(results) < n:
        candidate = random_clifford_matrix()
        index = np.unravel_index(np.argmax(np.abs(candidate)), candidate.shape)
        aligned_candidate = candidate * np.exp(-1j * np.angle(candidate[index]))
        aligned_original = original * np.exp(-1j * np.angle(original[index]))

        if np.allclose(
            aligned_candidate, aligned_original, rtol=0.4, atol=0.4
        ):
            with qml.QueuingManager.stop_recording():
                operation = qml.QubitUnitary(candidate, wires=wires)
            results.append(qml.tape.QuantumScript([operation]))

    return results
