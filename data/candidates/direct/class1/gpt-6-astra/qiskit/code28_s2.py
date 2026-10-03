# EVAL_META: task_id=28, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def visualize_bell_states():
    simulator = AerSimulator()
    circuits = []
    for name in ("phi_plus", "phi_minus"):
        circuit = QuantumCircuit(2, 2, name=name)
        circuit.h(0)
        circuit.cx(0, 1)
        if name == "phi_minus":
            circuit.z(0)
        circuit.measure([0, 1], [0, 1])
        circuits.append(circuit)

    compiled = transpile(circuits, simulator, seed_transpiler=28)
    result = simulator.run(
        compiled, shots=4096, seed_simulator=28
    ).result()

    distributions = {}
    for index, name in enumerate(("phi_plus", "phi_minus")):
        counts = result.get_counts(index)
        total = sum(counts.values())
        distributions[name] = {
            bitstring: count / total
            for bitstring, count in sorted(counts.items())
        }
    return distributions
