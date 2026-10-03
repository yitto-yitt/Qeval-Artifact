# EVAL_META: task_id=28, framework=pennylane, class=1
import pennylane as qml

def visualize_bell_states():
    shots = 1000
    dev = qml.device("default.qubit", wires=2, shots=shots)

    @qml.qnode(dev)
    def phi_plus():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.sample(wires=[0, 1])

    @qml.qnode(dev)
    def phi_minus():
        qml.PauliX(wires=0)
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.sample(wires=[0, 1])

    def to_dist(samples):
        counts = {}
        for s in samples:
            bits = "".join(str(int(b)) for b in s)
            counts[bits] = counts.get(bits, 0) + 1
        total = sum(counts.values())
        return {k: v / total for k, v in counts.items()}

    return {
        "phi_plus": to_dist(phi_plus()),
        "phi_minus": to_dist(phi_minus()),
    }
