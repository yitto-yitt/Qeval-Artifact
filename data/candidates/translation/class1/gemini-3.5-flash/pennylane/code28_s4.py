# EVAL_META: task_id=28, framework=pennylane, class=1
import pennylane as qml

def visualize_bell_states():
    dev = qml.device("default.qubit", shots=1000)
    
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

    counts_plus = circuit_phi_plus()
    counts_minus = circuit_phi_minus()
    
    total_plus = sum(counts_plus.values())
    total_minus = sum(counts_minus.values())
    
    return {
        "phi_plus": {k: v / total_plus for k, v in counts_plus.items()},
        "phi_minus": {k: v / total_minus for k, v in counts_minus.items()}
    }
