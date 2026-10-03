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

    def counts_from_samples(samples):
        counts = {}
        for s in samples:
            key = "".join(str(int(b)) for b in s)
            counts[key] = counts.get(key, 0) + 1
        return counts

    phi_plus_counts = counts_from_samples(phi_plus_circuit())
    phi_minus_counts = counts_from_samples(phi_minus_circuit())

    phi_plus_total = sum(phi_plus_counts.values())
    phi_minus_total = sum(phi_minus_counts.values())

    return {
        "phi_plus": {k: v / phi_plus_total for k, v in phi_plus_counts.items()},
        "phi_minus": {k: v / phi_minus_total for k, v in phi_minus_counts.items()},
    }
