# EVAL_META: task_id=28, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def visualize_bell_states():
    circuits = []
    labels = ("phi_plus", "phi_minus")

    for label in labels:
        circuit = QuantumCircuit(2, 2)
        circuit.h(0)
        circuit.cx(0, 1)
        if label == "phi_minus":
            circuit.z(0)
        circuit.measure([0, 1], [0, 1])
        circuits.append(circuit)

    simulator = AerSimulator()
    compiled = transpile(circuits, simulator, seed_transpiler=28)
    result = simulator.run(
        compiled, shots=4096, seed_simulator=28
    ).result()

    distributions = {}
    for index, label in enumerate(labels):
        counts = result.get_counts(index)
        total = sum(counts.values())
        distributions[label] = {
            bitstring: count / total
            for bitstring, count in sorted(counts.items())
        }

    return distributions
