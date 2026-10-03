# EVAL_META: task_id=110, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def equivalent_clifford_circuit(circuit, n):
    if n <= 0:
        return []

    if isinstance(circuit, qml.tape.QuantumScript):
        tape = circuit
    elif isinstance(circuit, qml.QNode):
        tape = qml.workflow.construct_tape(circuit)()
    elif isinstance(circuit, qml.operation.Operator):
        tape = qml.tape.QuantumScript([circuit])
    elif callable(circuit):
        tape = qml.tape.make_qscript(circuit)()
    else:
        raise TypeError("Expected a PennyLane circuit, QNode, or QuantumScript.")

    wires = list(tape.wires)
    num_qubits = len(wires)
    dimension = 1 << num_qubits
    unitary_tape = qml.tape.QuantumScript(tape.operations)
    target = np.asarray(
        qml.matrix(unitary_tape, wire_order=wires), dtype=complex
    )
    rng = np.random.default_rng()
    indices = np.arange(dimension, dtype=np.int64)

    def symplectic(a, b):
        return int(
            (
                np.dot(a[:num_qubits], b[num_qubits:])
                + np.dot(a[num_qubits:], b[:num_qubits])
            )
            % 2
        )

    def independent_rows(rows):
        pivots = {}
        selected = []
        for row in rows:
            reduced = row.copy()
            for pivot in sorted(pivots):
                if reduced[pivot]:
                    reduced ^= pivots[pivot]
            nonzero = np.flatnonzero(reduced)
            if nonzero.size:
                pivots[int(nonzero[0])] = reduced
                selected.append(row.copy())
        return np.asarray(selected, dtype=np.int64).reshape(
            -1, 2 * num_qubits
        )

    def pauli_action(vector, pauli, sign):
        x = pauli[:num_qubits]
        z = pauli[num_qubits:]
        x_mask = 0
        parity = np.zeros(dimension, dtype=np.int64)
        for qubit in range(num_qubits):
            bit = 1 << (num_qubits - 1 - qubit)
            if x[qubit]:
                x_mask |= bit
            if z[qubit]:
                parity ^= (indices & bit) != 0
        phases = sign * (1j ** int(np.dot(x, z))) * (1 - 2 * parity)
        result = np.empty_like(vector, dtype=complex)
        if vector.ndim == 1:
            result[indices ^ x_mask] = phases * vector
        else:
            result[indices ^ x_mask, :] = phases[:, None] * vector
        return result

    def random_clifford_matrix():
        if num_qubits == 0:
            return np.ones((1, 1), dtype=complex)

        basis = np.eye(2 * num_qubits, dtype=np.int64)
        x_generators = []
        z_generators = []

        for _ in range(num_qubits):
            coefficients = rng.integers(0, 2, size=len(basis))
            while not np.any(coefficients):
                coefficients = rng.integers(0, 2, size=len(basis))
            x = (coefficients @ basis) % 2

            pairings = np.array(
                [symplectic(x, row) for row in basis], dtype=np.int64
            )
            coefficients = rng.integers(0, 2, size=len(basis))
            if int(np.dot(coefficients, pairings) % 2) == 0:
                coefficients[int(np.flatnonzero(pairings)[0])] ^= 1
            z = (coefficients @ basis) % 2

            x_generators.append((x, 1 - 2 * int(rng.integers(2))))
            z_generators.append((z, 1 - 2 * int(rng.integers(2))))

            projected = [
                row
                ^ (symplectic(row, z) * x)
                ^ (symplectic(row, x) * z)
                for row in basis
            ]
            basis = independent_rows(projected)

        projector = np.eye(dimension, dtype=complex)
        for pauli, sign in z_generators:
            projector = (
                projector + pauli_action(projector, pauli, sign)
            ) / 2

        column = int(np.argmax(np.real(np.diag(projector))))
        state = projector[:, column].copy()
        state /= np.linalg.norm(state)

        matrix = np.empty((dimension, dimension), dtype=complex)
        matrix[:, 0] = state
        for column in range(1, dimension):
            bit = column & -column
            qubit = num_qubits - bit.bit_length()
            pauli, sign = x_generators[qubit]
            matrix[:, column] = pauli_action(
                matrix[:, column ^ bit], pauli, sign
            )
        return matrix

    results = []
    while len(results) < n:
        matrix = random_clifford_matrix()
        pivot = np.unravel_index(np.argmax(np.abs(matrix)), matrix.shape)
        aligned_matrix = matrix * np.exp(-1j * np.angle(matrix[pivot]))
        aligned_target = target * np.exp(-1j * np.angle(target[pivot]))
        if np.allclose(aligned_matrix, aligned_target, rtol=0.4, atol=0.4):
            with qml.QueuingManager.stop_recording():
                operations = (
                    [qml.QubitUnitary(matrix, wires=wires)] if wires else []
                )
                results.append(qml.tape.QuantumScript(operations))

    return results
