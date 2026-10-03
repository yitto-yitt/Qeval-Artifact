# EVAL_META: task_id=28, framework=pennylane, class=1
import pennylane as qml

def visualize_bell_states():
    dev = qml.device("default.qubit", wires=2, shots=1000)

    @qml.qnode(dev)
    def phi_plus_circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.counts()

    @qml.qnode(dev)
    def phi_minus_circuit():
        qml.PauliX(wires=0)
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.counts()

    counts_plus = phi_plus_circuit()
    counts_minus = phi_minus_circuit()
    total_plus = sum(counts_plus.values())
    total_minus = sum(counts_minus.values())
    phi_plus_probs = {key: value / total_plus for key, value in counts_plus.items()}
    phi_minus_probs = {key: value / total_minus for key, value in counts_minus.items()}
    return {
        "phi_plus": phi_plus_probs,
        "phi_minus": phi_minus_probs,
    }
