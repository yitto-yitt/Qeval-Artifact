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
        
    samples_plus = phi_plus_circuit()
    samples_minus = phi_minus_circuit()
    
    def get_probs(samples):
        counts = {}
        for s in samples:
            # Qiskit orders bitstrings as q_{n-1} ... q_0
            # s[0] is q_0, s[1] is q_1
            bitstring = f"{int(s[1])}{int(s[0])}"
            counts[bitstring] = counts.get(bitstring, 0) + 1
        total = sum(counts.values())
        return {k: v / total for k, v in counts.items()}
        
    return {
        "phi_plus": get_probs(samples_plus),
        "phi_minus": get_probs(samples_minus)
    }
