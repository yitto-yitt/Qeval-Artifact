# EVAL_META: task_id=110, framework=cirq, class=3
import random
import cirq

def equivalent_clifford_circuit(circuit, n):
    qubits = list(circuit.all_qubits())
    try:
        qubits = sorted(qubits)
    except TypeError:
        pass

    count = int(n)
    if count <= 0:
        return []

    if not qubits:
        return [cirq.Circuit(circuit) for _ in range(count)]

    def random_clifford_op():
        if len(qubits) >= 2 and random.random() < 0.45:
            q0, q1 = random.sample(qubits, 2)
            gate = random.choice(("cnot", "cz", "swap"))
            if gate == "cnot":
                return cirq.CNOT(q0, q1)
            if gate == "cz":
                return cirq.CZ(q0, q1)
            return cirq.SWAP(q0, q1)
        q = random.choice(qubits)
        gate = random.choice((cirq.X, cirq.Y, cirq.Z, cirq.H, cirq.S))
        return gate(q)

    def append_identity_gadgets(target, number):
        for _ in range(number):
            op = random_clifford_op()
            inv = cirq.inverse(op)
            if random.random() < 0.5:
                first, second = op, inv
            else:
                first, second = inv, op
            target.append(first, strategy=cirq.InsertStrategy.NEW)
            target.append(second, strategy=cirq.InsertStrategy.NEW)

    base = cirq.Circuit(circuit)
    circuits = []

    for _ in range(count):
        total_gadgets = random.randint(1, max(2, 2 * len(qubits) + 2))
        prefix_gadgets = random.randint(0, total_gadgets)

        prefix = cirq.Circuit()
        suffix = cirq.Circuit()

        append_identity_gadgets(prefix, prefix_gadgets)
        append_identity_gadgets(suffix, total_gadgets - prefix_gadgets)

        circuits.append(prefix + base + suffix)

    return circuits
