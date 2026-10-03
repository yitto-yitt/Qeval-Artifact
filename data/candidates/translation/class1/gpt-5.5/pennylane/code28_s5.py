# EVAL_META: task_id=28, framework=pennylane, class=1
import pennylane as qml
from collections import Counter

def visualize_bell_states():
    shots = 1000
    dev_phi_plus = qml.device("default.qubit", wires=2, shots=shots)
    dev_phi_minus = qml.device("default.qubit", wires=2, shots=shots)

    @qml.qnode(dev_phi_plus)
    def phi_plus_circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.sample(wires=[0, 1])

    @qml.qnode(dev_phi_minus)
    def phi_minus_circuit():
        qml.PauliX(wires=0)
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.sample(wires=[0, 1])

    def samples_to_probabilities(samples):
        bitstrings = ["".join(str(int(bit)) for bit in sample) for sample in samples]
        counts = Counter(bitstrings)
        total = sum(counts.values())
        return {key: value / total for key, value in counts.items()}

    return {
        "phi_plus": samples_to_probabilities(phi_plus_circuit()),
        "phi_minus": samples_to_probabilities(phi_minus_circuit()),
    }
