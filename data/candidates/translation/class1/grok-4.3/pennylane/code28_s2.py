# EVAL_META: task_id=28, framework=pennylane, class=1
import pennylane as qml

def visualize_bell_states():
    shots = 1000
    dev = qml.device("default.qubit", wires=2, shots=shots)

    @qml.qnode(dev)
    def circuit_phi_plus():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.counts()

    @qml.qnode(dev)
    def circuit_phi_minus():
        qml.PauliX(wires=0)
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.counts()

    counts_plus = circuit_phi_plus()
    counts_minus = circuit_phi_minus()
    total_plus = sum(counts_plus.values())
    total_minus = sum(counts_minus.values())
    prob_plus = {k: v / total_plus for k, v in counts_plus.items()}
    prob_minus = {k: v / total_minus for k, v in counts_minus.items()}
    return {
        "phi_plus": prob_plus,
        "phi_minus": prob_minus,
    }
