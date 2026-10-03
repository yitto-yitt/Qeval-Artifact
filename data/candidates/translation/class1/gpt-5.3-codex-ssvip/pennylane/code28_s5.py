# EVAL_META: task_id=28, framework=pennylane, class=1
import pennylane as qml


def visualize_bell_states():
    shots = 1000
    dev = qml.device("default.qubit", wires=2, shots=shots)

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

    phi_plus_samples = phi_plus_circuit()
    phi_minus_samples = phi_minus_circuit()

    def samples_to_probs(samples):
        counts = {}
        for s in samples:
            bitstring = f"{int(s[1])}{int(s[0])}"
            counts[bitstring] = counts.get(bitstring, 0) + 1
        total = sum(counts.values())
        return {k: v / total for k, v in counts.items()}

    return {
        "phi_plus": samples_to_probs(phi_plus_samples),
        "phi_minus": samples_to_probs(phi_minus_samples),
    }
