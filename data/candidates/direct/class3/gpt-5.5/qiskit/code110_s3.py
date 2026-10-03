# EVAL_META: task_id=110, framework=qiskit, class=3
import random


def equivalent_clifford_circuit(circuit, n):
    rng = random.Random()
    results = []
    count = int(n)

    for _ in range(count):
        qc = circuit.copy()
        num_qubits = qc.num_qubits

        if num_qubits > 0:
            layers = rng.randint(1, max(2, 2 * num_qubits + 3))

            for _ in range(layers):
                if num_qubits == 1:
                    choice = rng.randrange(7)
                else:
                    choice = rng.randrange(11)

                if choice == 0:
                    q = rng.randrange(num_qubits)
                    qc.h(q)
                    qc.h(q)
                elif choice == 1:
                    q = rng.randrange(num_qubits)
                    qc.x(q)
                    qc.x(q)
                elif choice == 2:
                    q = rng.randrange(num_qubits)
                    qc.y(q)
                    qc.y(q)
                elif choice == 3:
                    q = rng.randrange(num_qubits)
                    qc.z(q)
                    qc.z(q)
                elif choice == 4:
                    q = rng.randrange(num_qubits)
                    qc.s(q)
                    qc.sdg(q)
                elif choice == 5:
                    q = rng.randrange(num_qubits)
                    qc.sdg(q)
                    qc.s(q)
                elif choice == 6:
                    q = rng.randrange(num_qubits)
                    qc.h(q)
                    qc.s(q)
                    qc.sdg(q)
                    qc.h(q)
                elif choice == 7:
                    q0, q1 = rng.sample(range(num_qubits), 2)
                    qc.cx(q0, q1)
                    qc.cx(q0, q1)
                elif choice == 8:
                    q0, q1 = rng.sample(range(num_qubits), 2)
                    qc.cz(q0, q1)
                    qc.cz(q0, q1)
                elif choice == 9:
                    q0, q1 = rng.sample(range(num_qubits), 2)
                    qc.swap(q0, q1)
                    qc.swap(q0, q1)
                else:
                    q0, q1 = rng.sample(range(num_qubits), 2)
                    qc.h(q1)
                    qc.cx(q0, q1)
                    qc.cx(q0, q1)
                    qc.h(q1)

        results.append(qc)

    return results
