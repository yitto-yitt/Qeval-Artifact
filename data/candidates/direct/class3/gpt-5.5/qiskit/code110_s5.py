# EVAL_META: task_id=110, framework=qiskit, class=3
import random


def equivalent_clifford_circuit(circuit, n):
    rng = random.SystemRandom()
    circuits = []
    num_qubits = circuit.num_qubits

    for _ in range(int(n)):
        qc = circuit.copy()

        if num_qubits > 0:
            block_count = rng.randint(max(1, num_qubits), max(2, 4 * num_qubits + 8))

            for _ in range(block_count):
                if num_qubits == 1:
                    choice = rng.choice(("h", "x", "y", "z", "s"))
                else:
                    choice = rng.choice(("h", "x", "y", "z", "s", "cx", "cz", "swap"))

                if choice == "h":
                    q = rng.randrange(num_qubits)
                    qc.h(q)
                    qc.h(q)
                elif choice == "x":
                    q = rng.randrange(num_qubits)
                    qc.x(q)
                    qc.x(q)
                elif choice == "y":
                    q = rng.randrange(num_qubits)
                    qc.y(q)
                    qc.y(q)
                elif choice == "z":
                    q = rng.randrange(num_qubits)
                    qc.z(q)
                    qc.z(q)
                elif choice == "s":
                    q = rng.randrange(num_qubits)
                    if rng.randrange(2):
                        qc.s(q)
                        qc.sdg(q)
                    else:
                        qc.sdg(q)
                        qc.s(q)
                elif choice == "cx":
                    q0, q1 = rng.sample(range(num_qubits), 2)
                    qc.cx(q0, q1)
                    qc.cx(q0, q1)
                elif choice == "cz":
                    q0, q1 = rng.sample(range(num_qubits), 2)
                    qc.cz(q0, q1)
                    qc.cz(q0, q1)
                else:
                    q0, q1 = rng.sample(range(num_qubits), 2)
                    qc.swap(q0, q1)
                    qc.swap(q0, q1)

        circuits.append(qc)

    return circuits
