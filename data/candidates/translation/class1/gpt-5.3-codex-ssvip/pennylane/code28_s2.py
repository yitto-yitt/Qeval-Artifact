# EVAL_META: task_id=28, framework=pennylane, class=1
import pennylane as qml


def visualize_bell_states():
    shots = 1000
    dev_plus = qml.device("default.qubit", wires=2, shots=shots)
    dev_minus = qml.device("default.qubit", wires=2, shots=shots)

    @qml.qnode(dev_plus)
    def phi_plus_circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.sample(wires=[0, 1])

    @qml.qnode(dev_minus)
    def phi_minus_circuit():
        qml.PauliX(wires=0)
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.sample(wires=[0, 1])

    def samples_to_probs(samples):
        counts = {}
        for s in samples:
            bitstring = "".join(str(int(b)) for b in s)
            counts[bitstring] = counts.get(bitstring, 0) + 1
        total = sum(counts.values())
        return {k: v / total for k, v in counts.items()}

    phi_plus_samples = phi_plus_circuit()
    phi_minus_samples = phi_minus_circuit()

    return {
        "phi_plus": samples_to_probs(phi_plus_samples),
        "phi_minus": samples_to_probs(phi_minus_samples),
    }
