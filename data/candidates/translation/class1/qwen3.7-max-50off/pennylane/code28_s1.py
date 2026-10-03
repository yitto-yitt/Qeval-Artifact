# EVAL_META: task_id=28, framework=pennylane, class=1
import pennylane as qml

dev = qml.device("default.qubit", shots=1000)

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

def visualize_bell_states():
    samples_plus = phi_plus_circuit()
    samples_minus = phi_minus_circuit()
    
    def get_probs(samples):
        counts = {}
        for s in samples:
            key = "".join(str(int(x)) for x in s)
            counts[key] = counts.get(key, 0) + 1
        total = sum(counts.values())
        return {k: v / total for k, v in counts.items()}

    return {
        "phi_plus": get_probs(samples_plus),
        "phi_minus": get_probs(samples_minus)
    }
