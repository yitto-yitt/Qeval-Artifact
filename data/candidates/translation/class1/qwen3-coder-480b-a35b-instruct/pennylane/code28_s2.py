# EVAL_META: task_id=28, framework=pennylane, class=1
import pennylane as qml
from collections import Counter

def visualize_bell_states():
    dev = qml.device("default.qubit", wires=2, shots=1000)

    @qml.qnode(dev)
    def circuit_phi_plus():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.sample()

    @qml.qnode(dev)
    def circuit_phi_minus():
        qml.PauliX(wires=0)
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.sample()

    samples_phi_plus = circuit_phi_plus()
    samples_phi_minus = circuit_phi_minus()

    # Convert samples to bitstrings
    bitstrings_phi_plus = []
    for sample in samples_phi_plus.T:
        bitstring = ''.join(map(str, sample.astype(int)))
        bitstrings_phi_plus.append(bitstring)

    bitstrings_phi_minus = []
    for sample in samples_phi_minus.T:
        bitstring = ''.join(map(str, sample.astype(int)))
        bitstrings_phi_minus.append(bitstring)

    # Count occurrences
    counts_phi_plus = Counter(bitstrings_phi_plus)
    counts_phi_minus = Counter(bitstrings_phi_minus)

    # Normalize to get probabilities
    total_phi_plus = sum(counts_phi_plus.values())
    total_phi_minus = sum(counts_phi_minus.values())

    prob_dist_phi_plus = {key: value / total_phi_plus for key, value in counts_phi_plus.items()}
    prob_dist_phi_minus = {key: value / total_phi_minus for key, value in counts_phi_minus.items()}

    return {
        "phi_plus": prob_dist_phi_plus,
        "phi_minus": prob_dist_phi_minus
    }
