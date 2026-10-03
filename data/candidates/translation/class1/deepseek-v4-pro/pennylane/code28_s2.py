# EVAL_META: task_id=28, framework=pennylane, class=1
import pennylane as qml

def visualize_bell_states():
    dev = qml.device("default.qubit", wires=2, shots=1000)

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

    def _samples_to_probs(samples):
        counts = {}
        for sample in samples:
            bitstring = "".join(str(int(bit)) for bit in sample)
            counts[bitstring] = counts.get(bitstring, 0) + 1
        total = len(samples)
        return {key: value / total for key, value in counts.items()}

    return {
        "phi_plus": _samples_to_probs(phi_plus_circuit()),
        "phi_minus": _samples_to_probs(phi_minus_circuit()),
    }
