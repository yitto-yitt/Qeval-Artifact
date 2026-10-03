# EVAL_META: task_id=110, framework=cirq, class=3
import random
import cirq


def equivalent_clifford_circuit(circuit, n):
    qubits = list(circuit.all_qubits())
    circuits = []

    if not qubits:
        return [circuit.copy() for _ in range(n)]

    one_qubit_pairs = [
        lambda q: [cirq.H(q), cirq.H(q)],
        lambda q: [cirq.X(q), cirq.X(q)],
        lambda q: [cirq.Y(q), cirq.Y(q)],
        lambda q: [cirq.Z(q), cirq.Z(q)],
        lambda q: [cirq.S(q), cirq.S(q) ** -1],
        lambda q: [cirq.S(q) ** -1, cirq.S(q)],
    ]

    two_qubit_pairs = [
        lambda a, b: [cirq.CNOT(a, b), cirq.CNOT(a, b)],
        lambda a, b: [cirq.CZ(a, b), cirq.CZ(a, b)],
        lambda a, b: [cirq.SWAP(a, b), cirq.SWAP(a, b)],
    ]

    for _ in range(n):
        qc = cirq.Circuit()
        prefix_len = random.randint(0, max(1, 2 * len(qubits)))
        suffix_len = random.randint(1, max(2, 3 * len(qubits)))

        for _ in range(prefix_len):
            if len(qubits) >= 2 and random.random() < 0.45:
                a, b = random.sample(qubits, 2)
                qc.append(random.choice(two_qubit_pairs)(a, b))
            else:
                q = random.choice(qubits)
                qc.append(random.choice(one_qubit_pairs)(q))

        qc += circuit.copy()

        for _ in range(suffix_len):
            if len(qubits) >= 2 and random.random() < 0.45:
                a, b = random.sample(qubits, 2)
                qc.append(random.choice(two_qubit_pairs)(a, b))
            else:
                q = random.choice(qubits)
                qc.append(random.choice(one_qubit_pairs)(q))

        circuits.append(qc)

    return circuits
