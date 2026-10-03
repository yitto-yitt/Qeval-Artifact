# EVAL_META: task_id=28, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def visualize_bell_states():
    shots = 4096
    simulator = AerSimulator(seed_simulator=28)

    phi_plus = QuantumCircuit(2, 2)
    phi_plus.h(0)
    phi_plus.cx(0, 1)
    phi_plus.measure([0, 1], [0, 1])

    phi_minus = QuantumCircuit(2, 2)
    phi_minus.h(0)
    phi_minus.cx(0, 1)
    phi_minus.z(0)
    phi_minus.measure([0, 1], [0, 1])

    circuits = transpile([phi_plus, phi_minus], simulator)
    result = simulator.run(circuits, shots=shots).result()

    def probabilities(index):
        counts = result.get_counts(index)
        return {bitstring: counts.get(bitstring, 0) / shots for bitstring in sorted(counts)}

    return {
        "phi_plus": probabilities(0),
        "phi_minus": probabilities(1),
    }
