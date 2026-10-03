# EVAL_META: task_id=28, framework=pennylane, class=1
import pennylane as qml

def visualize_bell_states():
    dev = qml.device("default.qubit", wires=2, shots=1000)

    @qml.qnode(dev)
    def phi_plus():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.counts(wires=[0, 1])

    @qml.qnode(dev)
    def phi_minus():
        qml.PauliX(wires=0)
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.counts(wires=[0, 1])

    phi_plus_counts = phi_plus()
    phi_minus_counts = phi_minus()

    phi_plus_total = sum(phi_plus_counts.values())
    phi_minus_total = sum(phi_minus_counts.values())

    return {
        "phi_plus": {key: value / phi_plus_total for key, value in phi_plus_counts.items()},
        "phi_minus": {key: value / phi_minus_total for key, value in phi_minus_counts.items()},
    }
