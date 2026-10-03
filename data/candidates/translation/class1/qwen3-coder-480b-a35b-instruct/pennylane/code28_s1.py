# EVAL_META: task_id=28, framework=pennylane, class=1
import pennylane as qml
from collections import Counter

def visualize_bell_states():
    dev = qml.device('default.qubit', wires=2, shots=1000)

    @qml.qnode(dev)
    def phi_plus_circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.sample(wires=[0, 1])

    @qml.qnode(dev)
    def phi_minus_circuit():
        qml.PauliX(wires=0)
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.sample(wires=[0, 1])

    # Run circuits
    phi_plus_samples = phi_plus_circuit()
    phi_minus_samples = phi_minus_circuit()

    # Convert samples to bitstrings and count
    phi_plus_bitstrings = [''.join(map(str, sample)) for sample in phi_plus_samples]
    phi_minus_bitstrings = [''.join(map(str, sample)) for sample in phi_minus_samples]

    phi_plus_counts = Counter(phi_plus_bitstrings)
    phi_minus_counts = Counter(phi_minus_bitstrings)

    # Normalize to get probabilities
    phi_plus_total = sum(phi_plus_counts.values())
    phi_minus_total = sum(phi_minus_counts.values())

    phi_plus_probs = {key: value / phi_plus_total for key, value in phi_plus_counts.items()}
    phi_minus_probs = {key: value / phi_minus_total for key, value in phi_minus_counts.items()}

    return {
        "phi_plus": phi_plus_probs,
        "phi_minus": phi_minus_probs
    }
