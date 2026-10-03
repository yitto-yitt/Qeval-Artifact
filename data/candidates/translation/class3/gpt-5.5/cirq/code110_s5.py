# EVAL_META: task_id=110, framework=cirq, class=3
import random
import cirq

def equivalent_clifford_circuit(circuit, n):
    qubits = sorted(circuit.all_qubits())
    circuits = []
    single_qubit_gates = [cirq.X, cirq.Y, cirq.Z, cirq.H, cirq.S]
    two_qubit_gates = [cirq.CNOT, cirq.CZ, cirq.SWAP]

    for _ in range(n):
        qc = cirq.Circuit(circuit)

        if qubits:
            repetitions = random.randint(1, max(1, 3 * len(qubits)))
            for _ in range(repetitions):
                if len(qubits) >= 2 and random.random() < 0.35:
                    q0, q1 = random.sample(qubits, 2)
                    gate = random.choice(two_qubit_gates)
                    op = gate(q0, q1)
                else:
                    q = random.choice(qubits)
                    gate = random.choice(single_qubit_gates)
                    op = gate(q)

                qc.append(op)
                qc.append(cirq.inverse(op))

        circuits.append(qc)

    return circuits
