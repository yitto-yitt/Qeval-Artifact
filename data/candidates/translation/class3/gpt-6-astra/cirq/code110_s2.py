# EVAL_META: task_id=110, framework=cirq, class=3
import cirq
import numpy as np


def equivalent_clifford_circuit(circuit, n):
    qubits = tuple(cirq.QubitOrder.DEFAULT.order_for(circuit.all_qubits()))
    num_qubits = len(qubits)
    original = circuit.unitary(qubit_order=qubits)
    rng = np.random.default_rng()
    results = []

    def symplectic_products(vectors, vector):
        return (
            vectors[:, :num_qubits] @ vector[num_qubits:]
            + vectors[:, num_qubits:] @ vector[:num_qubits]
        ) % 2

    def independent_rows(matrix):
        matrix = matrix.copy()
        rank = 0
        for column in range(matrix.shape[1]):
            pivots = np.flatnonzero(matrix[rank:, column])
            if not pivots.size:
                continue
            pivot = rank + int(pivots[0])
            matrix[[rank, pivot]] = matrix[[pivot, rank]]
            for row in range(matrix.shape[0]):
                if row != rank and matrix[row, column]:
                    matrix[row] ^= matrix[rank]
            rank += 1
            if rank == matrix.shape[0]:
                break
        return matrix[:rank]

    while len(results) < n:
        if num_qubits == 0:
            candidate = cirq.Circuit()
        else:
            basis = np.eye(2 * num_qubits, dtype=np.uint8)
            images = np.zeros(
                (2 * num_qubits, 2 * num_qubits), dtype=np.uint8
            )

            for index in range(num_qubits):
                coefficients = rng.integers(
                    0, 2, size=len(basis), dtype=np.uint8
                )
                while not np.any(coefficients):
                    coefficients = rng.integers(
                        0, 2, size=len(basis), dtype=np.uint8
                    )
                x_image = (coefficients @ basis) % 2

                products = symplectic_products(basis, x_image)
                coefficients = rng.integers(
                    0, 2, size=len(basis), dtype=np.uint8
                )
                if int(coefficients @ products) % 2 == 0:
                    coefficients[int(np.flatnonzero(products)[0])] ^= 1
                z_image = (coefficients @ basis) % 2

                images[index] = x_image
                images[num_qubits + index] = z_image

                projected = (
                    basis
                    ^ np.outer(symplectic_products(basis, z_image), x_image)
                    ^ np.outer(symplectic_products(basis, x_image), z_image)
                )
                basis = independent_rows(projected)

            tableau = cirq.CliffordTableau(
                num_qubits,
                xs=images[:, :num_qubits].astype(bool),
                zs=images[:, num_qubits:].astype(bool),
                rs=rng.integers(
                    0, 2, size=2 * num_qubits, dtype=np.uint8
                ).astype(bool),
            )
            gate = cirq.CliffordGate.from_clifford_tableau(tableau)
            candidate = cirq.Circuit(cirq.decompose_once(gate.on(*qubits)))

        candidate_unitary = candidate.unitary(qubit_order=qubits)
        if cirq.linalg.allclose_up_to_global_phase(
            candidate_unitary, original, rtol=0.4, atol=0.4
        ):
            results.append(candidate)

    return results
