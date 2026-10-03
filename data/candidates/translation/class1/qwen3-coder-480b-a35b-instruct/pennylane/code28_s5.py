# EVAL_META: task_id=28, framework=pennylane, class=1
import pennylane as qml
from collections import Counter

def visualize_bell_states():
    dev = qml.device("default.qubit", wires=2, shots=1000)

    @qml.qnode(dev)
    def circuit_phi_plus():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.sample(qml.PauliZ(wires=0)), qml.sample(qml.PauliZ(wires=1))

    @qml.qnode(dev)
    def circuit_phi_minus():
        qml.PauliX(wires=0)
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.sample(qml.PauliZ(wires=0)), qml.sample(qml.PauliZ(wires=1))

    samples_phi_plus = circuit_phi_plus()
    samples_phi_minus = circuit_phi_minus()

    # Convert Z-basis samples to bitstrings (Z=+1 -> 0, Z=-1 -> 1)
    bitstrings_phi_plus = []
    for i in range(len(samples_phi_plus[0])):
        bit0 = '0' if samples_phi_plus[0][i] == 1 else '1'
        bit1 = '0' if samples_phi_plus[1][i] == 1 else '1'
        bitstrings_phi_plus.append(bit0 + bit1)

    bitstrings_phi_minus = []
    for i in range(len(samples_phi_minus[0])):
        bit0 = '0' if samples_phi_minus[0][i] == 1 else '1'
        bit1 = '0' if samples_phi_minus[1][i] == 1 else '1'
        bitstrings_phi_minus.append(bit0 + bit1)

    counts_phi_plus = Counter(bitstrings_phi_plus)
    counts_phi_minus = Counter(bitstrings_phi_minus)

    total_phi_plus = sum(counts_phi_plus.values())
    total_phi_minus = sum(counts_phi_minus.values())

    prob_dist_phi_plus = {key: value / total_phi_plus for key, value in counts_phi_plus.items()}
    prob_dist_phi_minus = {key: value / total_phi_minus for key, value in counts_phi_minus.items()}

    return {
        "phi_plus": prob_dist_phi_plus,
        "phi_minus": prob_dist_phi_minus
    }
