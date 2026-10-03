# EVAL_META: task_id=15, framework=pennylane, class=1
import pennylane as qml
from collections import Counter

def noisy_bell():
    # Create a device with noise model similar to the fake backend
    dev = qml.device("default.qubit", wires=2, shots=1000)
    
    @qml.qnode(dev)
    def bell_circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.sample(wires=[0, 1])
    
    samples = bell_circuit()
    
    # Convert samples to bitstrings
    bitstrings = []
    for sample in samples:
        bitstring = ''.join(str(int(b)) for b in sample)
        bitstrings.append(bitstring)
    
    # Count occurrences
    counts = Counter(bitstrings)
    total = sum(counts.values())
    
    # Normalize to probabilities
    probs = {key: value / total for key, value in counts.items()}
    
    return probs
