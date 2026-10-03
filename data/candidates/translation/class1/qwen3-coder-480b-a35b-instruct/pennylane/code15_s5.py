# EVAL_META: task_id=15, framework=pennylane, class=1
import pennylane as qml
from collections import Counter

def noisy_bell():
    # Create a device with noise similar to a real backend
    dev = qml.device("default.mixed", wires=2, shots=1000)

    @qml.qnode(dev)
    def bell_circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.sample(wires=[0, 1])

    # Execute the circuit
    samples = bell_circuit()

    # Convert samples to bitstrings
    bitstrings = []
    for sample in samples:
        bitstring = ''.join(str(int(bit)) for bit in sample)
        bitstrings.append(bitstring)

    # Count occurrences of each bitstring
    counts = Counter(bitstrings)
    
    # Calculate probabilities
    total = len(bitstrings)
    prob_dist = {bitstring: count / total for bitstring, count in counts.items()}
    
    return prob_dist
