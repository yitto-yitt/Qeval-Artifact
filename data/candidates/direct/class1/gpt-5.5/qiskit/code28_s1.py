# EVAL_META: task_id=28, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def visualize_bell_states():
    shots = 4096
    seed = 28

    phi_plus = QuantumCircuit(2, 2)
    phi_plus.h(0)
    phi_plus.cx(0, 1)
    phi_plus.measure([0, 1], [0, 1])

    phi_minus = QuantumCircuit(2, 2)
    phi_minus.h(0)
    phi_minus.cx(0, 1)
    phi_minus.z(0)
    phi_minus.measure([0, 1], [0, 1])

    backend = AerSimulator(seed_simulator=seed)
    circuits = transpile([phi_plus, phi_minus], backend)
    result = backend.run(circuits, shots=shots).result()

    bitstrings = ["00", "01", "10", "11"]

    def probabilities(index):
        counts = result.get_counts(index)
        return {bitstring: counts.get(bitstring, 0) / shots for bitstring in bitstrings}

    return {
        "phi_plus": probabilities(0),
        "phi_minus": probabilities(1),
    }
