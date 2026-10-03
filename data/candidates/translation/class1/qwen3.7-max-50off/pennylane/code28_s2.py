# EVAL_META: task_id=28, framework=pennylane, class=1
import pennylane as qml

dev = qml.device("default.qubit", wires=2, shots=1000)

@qml.qnode(dev)
def circuit_phi_plus():
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0, 1])
    return qml.counts(wires=[0, 1])

@qml.qnode(dev)
def circuit_phi_minus():
    qml.PauliX(wires=0)
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0, 1])
    return qml.counts(wires=[0, 1])

def visualize_bell_states():
    counts_plus = circuit_phi_plus()
    counts_minus = circuit_phi_minus()
    
    def process_counts(counts):
        total = sum(counts.values())
        processed = {}
        for k, v in counts.items():
            if isinstance(k, tuple):
                key = "".join(str(x) for x in k)
            else:
                key = str(k)
            processed[key] = v / total
        return processed

    return {
        "phi_plus": process_counts(counts_plus),
        "phi_minus": process_counts(counts_minus)
    }
