# EVAL_META: task_id=110, framework=cirq, class=3
import random
import cirq


def equivalent_clifford_circuit(circuit, n):
    qubits = sorted(circuit.all_qubits())
    qc_list = []

    if not qubits:
        return [cirq.Circuit(circuit) for _ in range(n)]

    one_qubit_pairs = [
        lambda q: [cirq.X(q), cirq.X(q)],
        lambda q: [cirq.Y(q), cirq.Y(q)],
        lambda q: [cirq.Z(q), cirq.Z(q)],
        lambda q: [cirq.H(q), cirq.H(q)],
        lambda q: [cirq.S(q), cirq.S(q) ** -1],
        lambda q: [cirq.S(q) ** -1, cirq.S(q)],
    ]

    two_qubit_pairs = [
        lambda a, b: [cirq.CNOT(a, b), cirq.CNOT(a, b)],
        lambda a, b: [cirq.CZ(a, b), cirq.CZ(a, b)],
        lambda a, b: [cirq.SWAP(a, b), cirq.SWAP(a, b)],
    ]

    for i in range(n):
        qc = cirq.Circuit()
        prefix_pairs = random.randint(0, 3)
        suffix_pairs = random.randint(1, 6)

        for _ in range(prefix_pairs):
            if len(qubits) >= 2 and random.random() < 0.5:
                a, b = random.sample(qubits, 2)
                qc.append(random.choice(two_qubit_pairs)(a, b))
            else:
                q = random.choice(qubits)
                qc.append(random.choice(one_qubit_pairs)(q))

        qc += cirq.Circuit(circuit)

        for _ in range(suffix_pairs + (i % 3)):
            if len(qubits) >= 2 and random.random() < 0.5:
                a, b = random.sample(qubits, 2)
                qc.append(random.choice(two_qubit_pairs)(a, b))
            else:
                q = random.choice(qubits)
                qc.append(random.choice(one_qubit_pairs)(q))

        qc_list.append(qc)

    return qc_list
