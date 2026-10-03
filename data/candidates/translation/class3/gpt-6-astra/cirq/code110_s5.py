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

    def sample_complement(pairs):
        vector = rng.integers(0, 2, size=2 * num_qubits, dtype=np.int64)
        for x, z in pairs:
            coefficient_x = symplectic_product(vector, z)
            coefficient_z = symplectic_product(vector, x)
            vector ^= coefficient_x * x
            vector ^= coefficient_z * z
        return vector

    while len(results) < n:
        if num_qubits == 0:
            candidate = cirq.Circuit()
        else:
            pairs = []
            for _ in range(num_qubits):
                x = sample_complement(pairs)
                while not np.any(x):
                    x = sample_complement(pairs)

                z = sample_complement(pairs)
                while symplectic_product(x, z) != 1:
                    z = sample_complement(pairs)

                pairs.append((x, z))

            rows = np.array(
                [x for x, _ in pairs] + [z for _, z in pairs],
                dtype=bool,
            )
            tableau = cirq.CliffordTableau(
                num_qubits,
                rs=rng.integers(0, 2, size=2 * num_qubits).astype(bool),
                xs=rows[:, :num_qubits],
                zs=rows[:, num_qubits:],
            )
            gate = cirq.CliffordGate.from_clifford_tableau(tableau)
            candidate = cirq.Circuit(gate.on(*qubits))

        if cirq.linalg.allclose_up_to_global_phase(
            candidate.unitary(qubit_order=qubits),
            original,
            rtol=0.4,
            atol=0.4,
        ):
            results.append(cirq.Circuit(cirq.decompose(candidate)))

    return results
