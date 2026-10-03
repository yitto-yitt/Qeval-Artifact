# EVAL_META: task_id=28, framework=pennylane, class=1
import pennylane as qml
import numpy as np

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

    def samples_to_distribution(samples):
        counts = {}
        for sample in samples:
            bitstring = "".join(str(int(bit)) for bit in sample)
            counts[bitstring] = counts.get(bitstring, 0) + 1
        total = sum(counts.values())
        return {key: value / total for key, value in counts.items()}

    return {
        "phi_plus": samples_to_distribution(np.asarray(phi_plus_circuit())),
        "phi_minus": samples_to_distribution(np.asarray(phi_minus_circuit())),
    }
