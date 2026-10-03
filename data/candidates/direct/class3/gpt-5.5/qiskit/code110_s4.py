# EVAL_META: task_id=110, framework=qiskit, class=3
import random
from qiskit import QuantumCircuit


def equivalent_clifford_circuit(circuit, n):
    circuits = []
    num_qubits = circuit.num_qubits
    count = int(n)

    for _ in range(count):
        qc = circuit.copy()
        if num_qubits <= 0:
            circuits.append(qc)
            continue

        reps = random.randint(1, max(1, 4 * num_qubits + 4))

        for _ in range(reps):
            if num_qubits == 1:
                gate = random.choice(("h", "x", "y", "z", "s"))
            else:
                gate = random.choice(("h", "x", "y", "z", "s", "cx", "cz", "swap"))

            if gate == "h":
                q = random.randrange(num_qubits)
                qc.h(q)
                qc.h(q)
            elif gate == "x":
                q = random.randrange(num_qubits)
                qc.x(q)
                qc.x(q)
            elif gate == "y":
                q = random.randrange(num_qubits)
                qc.y(q)
                qc.y(q)
            elif gate == "z":
                q = random.randrange(num_qubits)
                qc.z(q)
                qc.z(q)
            elif gate == "s":
                q = random.randrange(num_qubits)
                if random.randrange(2):
                    qc.s(q)
                    qc.sdg(q)
                else:
                    qc.sdg(q)
                    qc.s(q)
            elif gate == "cx":
                q0, q1 = random.sample(range(num_qubits), 2)
                qc.cx(q0, q1)
                qc.cx(q0, q1)
            elif gate == "cz":
                q0, q1 = random.sample(range(num_qubits), 2)
                qc.cz(q0, q1)
                qc.cz(q0, q1)
            elif gate == "swap":
                q0, q1 = random.sample(range(num_qubits), 2)
                qc.swap(q0, q1)
                qc.swap(q0, q1)

        circuits.append(qc)

    return circuits
