# EVAL_META: task_id=14, framework=pennylane, class=1
import pennylane as qml

def bell_each_shot():
    dev = qml.device("default.qubit", wires=2, shots=10)
    
    @qml.qnode(dev)
    def bell_circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.sample(qml.PauliZ(wires=0)), qml.sample(qml.PauliZ(wires=1))
    
    samples = bell_circuit()
    
    # Convert samples to bitstrings
    bitstrings = []
    for i in range(samples.shape[1]):
        bitstring = ""
        for j in range(samples.shape[0]):
            bit = "0" if samples[j, i] == 1 else "1"
            bitstring += bit
        bitstrings.append(bitstring)
    
    # Count occurrences of each bitstring
    counts = {}
    for bitstring in bitstrings:
        counts[bitstring] = counts.get(bitstring, 0) + 1
    
    # Calculate probabilities
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
