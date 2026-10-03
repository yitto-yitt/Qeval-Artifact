# EVAL_META: task_id=110, framework=qiskit, class=3
import random
from qiskit import QuantumCircuit


def equivalent_clifford_circuit(circuit, n):
    circuits = []
    num_qubits = circuit.num_qubits

    for _ in range(n):
        new_circuit = circuit.copy()
        if num_qubits > 0:
            reps = random.randint(1, max(1, 3 * num_qubits))
            for _ in range(reps):
                if num_qubits >= 2 and random.random() < 0.35:
                    q1, q2 = random.sample(range(num_qubits), 2)
                    gate = random.choice(["cx", "cz", "swap"])
                    if gate == "cx":
                        new_circuit.cx(q1, q2)
                        new_circuit.cx(q1, q2)
                    elif gate == "cz":
                        new_circuit.cz(q1, q2)
                        new_circuit.cz(q1, q2)
                    else:
                        new_circuit.swap(q1, q2)
                        new_circuit.swap(q1, q2)
                else:
                    q = random.randrange(num_qubits)
                    gate = random.choice(["h", "x", "y", "z", "s", "sdg"])
                    if gate == "h":
                        new_circuit.h(q)
                        new_circuit.h(q)
                    elif gate == "x":
                        new_circuit.x(q)
                        new_circuit.x(q)
                    elif gate == "y":
                        new_circuit.y(q)
                        new_circuit.y(q)
                    elif gate == "z":
                        new_circuit.z(q)
                        new_circuit.z(q)
                    elif gate == "s":
                        new_circuit.s(q)
                        new_circuit.sdg(q)
                    else:
                        new_circuit.sdg(q)
                        new_circuit.s(q)
        circuits.append(new_circuit)

    return circuits
