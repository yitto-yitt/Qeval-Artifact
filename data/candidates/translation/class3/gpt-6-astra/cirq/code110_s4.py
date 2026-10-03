# EVAL_META: task_id=110, framework=cirq, class=3
import cirq
import numpy as np


def equivalent_clifford_circuit(circuit, n):
    qubits = tuple(cirq.QubitOrder.DEFAULT.order_for(circuit.all_qubits()))
    num_qubits = len(qubits)
    original = circuit.unitary(qubit_order=qubits)
    rng = np.random.default_rng()
    results = []

    def symplectic_product(a, b):
        return int(
            (
                np.dot(a[:num_qubits], b[num_qubits:])
                + np.dot(a[num_qubits:], b[:num_qubits])
            )
            % 2
        )

    def random_clifford():
        dimension = 2 * num_qubits
        basis = np.eye(dimension, dtype=np.int64)
        images_x = []
        images_z = []

        for _ in range(num_qubits):
            size = len(basis)
            coefficients = rng.integers(0, 2, size=size)
            while not np.any(coefficients):
                coefficients = rng.integers(0, 2, size=size)
            x = (coefficients @ basis) % 2

            z = (rng.integers(0, 2, size=size) @ basis) % 2
            while symplectic_product(x, z) != 1:
                z = (rng.integers(0, 2, size=size) @ basis) % 2

            images_x.append(x)
            images_z.append(z)

            independent = []
            pivots = []
            for row in basis:
                projected = (
                    row
                    + symplectic_product(row, z) * x
                    + symplectic_product(row, x) * z
                ) % 2
                for pivot, previous in zip(pivots, independent):
                    if projected[pivot]:
                        projected ^= previous
                nonzero = np.flatnonzero(projected)
                if nonzero.size:
                    pivots.append(int(nonzero[0]))
                    independent.append(projected)

            basis = np.asarray(independent, dtype=np.int64).reshape(
                -1, dimension
            )

        images = np.asarray(images_x + images_z, dtype=np.bool_)
        tableau = cirq.CliffordTableau(
            num_qubits,
            rs=rng.integers(0, 2, size=dimension).astype(np.bool_),
            xs=images[:, :num_qubits],
            zs=images[:, num_qubits:],
        )
        gate = cirq.CliffordGate.from_clifford_tableau(tableau)
        return cirq.Circuit(gate.on(*qubits))

    while len(results) < n:
        if num_qubits == 0:
            candidate = cirq.Circuit()
        else:
            candidate = random_clifford()
        candidate_unitary = candidate.unitary(qubit_order=qubits)
        if cirq.allclose_up_to_global_phase(
            candidate_unitary, original, rtol=0.4, atol=0.4
        ):
            results.append(candidate)

    return results
