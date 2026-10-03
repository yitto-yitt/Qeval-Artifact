# EVAL_META: task_id=110, framework=cirq, class=3
import cirq
import numpy as np


def equivalent_clifford_circuit(circuit, n):
    qubits = tuple(sorted(circuit.all_qubits()))
    num_qubits = len(qubits)
    original_unitary = circuit.unitary(qubit_order=qubits)
    rng = np.random.default_rng()
    results = []

    def symplectic_product(a, b):
        return int(
            (np.dot(a[:num_qubits], b[num_qubits:])
             + np.dot(a[num_qubits:], b[:num_qubits:])) % 2
        )

    def random_clifford_circuit():
        if num_qubits == 0:
            return cirq.Circuit()

        dimension = 2 * num_qubits
        basis = np.eye(dimension, dtype=np.uint8)
        generators = np.zeros((dimension, dimension), dtype=np.uint8)

        for i in range(num_qubits):
            while True:
                coefficients = rng.integers(
                    0, 2, size=len(basis), dtype=np.uint8
                )
                if np.any(coefficients):
                    v = (coefficients @ basis) % 2
                    break

            while True:
                coefficients = rng.integers(
                    0, 2, size=len(basis), dtype=np.uint8
                )
                w = (coefficients @ basis) % 2
                if symplectic_product(v, w):
                    break

            generators[i] = v
            generators[num_qubits + i] = w

            independent_rows = []
            pivots = []
            for row in basis:
                projected = row.copy()
                if symplectic_product(row, w):
                    projected ^= v
                if symplectic_product(row, v):
                    projected ^= w

                for pivot, existing in zip(pivots, independent_rows):
                    if projected[pivot]:
                        projected ^= existing

                nonzero = np.flatnonzero(projected)
                if nonzero.size:
                    pivots.append(int(nonzero[0]))
                    independent_rows.append(projected)

            basis = np.asarray(
                independent_rows, dtype=np.uint8
            ).reshape(-1, dimension)

        tableau = cirq.CliffordTableau(
            num_qubits,
            rs=rng.integers(0, 2, size=dimension).astype(bool),
            xs=generators[:, :num_qubits].astype(bool),
            zs=generators[:, num_qubits:].astype(bool),
        )
        gate = cirq.CliffordGate.from_clifford_tableau(tableau)
        candidate = cirq.Circuit(cirq.decompose(gate.on(*qubits)))
        candidate.append(cirq.I.on_each(*qubits))
        return candidate

    while len(results) < n:
        candidate = random_clifford_circuit()
        candidate_unitary = candidate.unitary(qubit_order=qubits)
        if cirq.linalg.allclose_up_to_global_phase(
            candidate_unitary,
            original_unitary,
            rtol=0.4,
            atol=0.4,
        ):
            results.append(candidate)

    return results
