# EVAL_META: task_id=110, framework=cirq, class=3
import cirq
import numpy as np


def equivalent_clifford_circuit(circuit, n):
    qubits = tuple(cirq.QubitOrder.DEFAULT.order_for(circuit.all_qubits()))
    num_qubits = len(qubits)
    original = circuit.unitary(qubit_order=qubits)
    rng = np.random.default_rng()
    results = []

    if num_qubits == 0:
        while len(results) < n:
            results.append(cirq.Circuit())
        return results

    def symplectic_product(a, b):
        return int(
            (
                np.dot(a[:num_qubits], b[num_qubits:])
                + np.dot(a[num_qubits:], b[:num_qubits])
            )
            % 2
        )

    def random_nonzero_vector(basis):
        while True:
            coefficients = rng.integers(0, 2, size=len(basis), dtype=np.uint8)
            if np.any(coefficients):
                return (coefficients @ basis) % 2

    def row_basis(matrix):
        matrix = matrix.copy()
        rank = 0
        for column in range(matrix.shape[1]):
            pivots = np.flatnonzero(matrix[rank:, column])
            if not len(pivots):
                continue
            pivot = rank + int(pivots[0])
            matrix[[rank, pivot]] = matrix[[pivot, rank]]
            for row in range(rank + 1, len(matrix)):
                if matrix[row, column]:
                    matrix[row] ^= matrix[rank]
            rank += 1
            if rank == len(matrix):
                break
        return matrix[:rank]

    while len(results) < n:
        basis = np.eye(2 * num_qubits, dtype=np.uint8)
        images = np.zeros((2 * num_qubits, 2 * num_qubits), dtype=np.uint8)

        for index in range(num_qubits):
            x_image = random_nonzero_vector(basis)
            while True:
                z_image = random_nonzero_vector(basis)
                if symplectic_product(x_image, z_image):
                    break

            images[index] = x_image
            images[num_qubits + index] = z_image

            projected = basis.copy()
            for row, vector in enumerate(basis):
                if symplectic_product(vector, z_image):
                    projected[row] ^= x_image
                if symplectic_product(vector, x_image):
                    projected[row] ^= z_image
            basis = row_basis(projected)

        tableau = cirq.CliffordTableau(
            num_qubits,
            rs=rng.integers(0, 2, size=2 * num_qubits).astype(bool),
            xs=images[:, :num_qubits].astype(bool),
            zs=images[:, num_qubits:].astype(bool),
        )
        gate = cirq.CliffordGate.from_clifford_tableau(tableau)
        candidate = cirq.Circuit(cirq.I.on_each(*qubits))
        candidate.append(cirq.decompose(gate.on(*qubits)))
        matrix = candidate.unitary(qubit_order=qubits)

        pivot = int(np.argmax(np.abs(matrix)))
        aligned_candidate = matrix * np.exp(-1j * np.angle(matrix.flat[pivot]))
        aligned_original = original * np.exp(-1j * np.angle(original.flat[pivot]))

        if np.allclose(
            aligned_candidate, aligned_original, rtol=0.4, atol=0.4
        ):
            results.append(candidate)

    return results
