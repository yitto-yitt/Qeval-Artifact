# EVAL_META: task_id=110, framework=qiskit, class=3
import random
from qiskit import QuantumCircuit


def equivalent_clifford_circuit(circuit, n):
    if not hasattr(circuit, "num_qubits") and hasattr(circuit, "to_circuit"):
        circuit = circuit.to_circuit()

    count = int(n)
    if count <= 0:
        return []

    num_qubits = circuit.num_qubits
    num_clbits = getattr(circuit, "num_clbits", 0)
    results = []

    for _ in range(count):
        if num_qubits == 0:
            results.append(circuit.copy())
            continue

        new_circuit = QuantumCircuit(num_qubits, num_clbits)
        repetitions = random.randint(max(1, num_qubits), max(2, 4 * num_qubits + 6))

        for _ in range(repetitions):
            if num_qubits > 1:
                gate_choice = random.randrange(8)
            else:
                gate_choice = random.randrange(5)

            q = random.randrange(num_qubits)

            if gate_choice == 0:
                new_circuit.x(q)
                new_circuit.x(q)
            elif gate_choice == 1:
                new_circuit.y(q)
                new_circuit.y(q)
            elif gate_choice == 2:
                new_circuit.z(q)
                new_circuit.z(q)
            elif gate_choice == 3:
                new_circuit.h(q)
                new_circuit.h(q)
            elif gate_choice == 4:
                new_circuit.s(q)
                new_circuit.sdg(q)
            elif gate_choice == 5:
                q0, q1 = random.sample(range(num_qubits), 2)
                new_circuit.cx(q0, q1)
                new_circuit.cx(q0, q1)
            elif gate_choice == 6:
                q0, q1 = random.sample(range(num_qubits), 2)
                new_circuit.cz(q0, q1)
                new_circuit.cz(q0, q1)
            else:
                q0, q1 = random.sample(range(num_qubits), 2)
                new_circuit.swap(q0, q1)
                new_circuit.swap(q0, q1)

        new_circuit.compose(
            circuit,
            qubits=list(range(num_qubits)),
            clbits=list(range(num_clbits)),
            inplace=True,
        )
        results.append(new_circuit)

    return results
