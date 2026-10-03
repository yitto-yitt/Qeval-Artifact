# EVAL_META: task_id=54, framework=pennylane, class=1
import pennylane as qml
from collections import Counter

def and_gate(a, b):
    a_bits = format(a, '03b')
    b_bits = format(b, '03b')
    
    dev = qml.device('default.qubit', wires=9, shots=None)
    
    @qml.qnode(dev)
    def circuit():
        # Initialize input registers based on a and b
        for i in range(3):
            if a_bits[2-i] == '1':
                qml.PauliX(wires=i)  # First 3 wires for a
            if b_bits[2-i] == '1':
                qml.PauliX(wires=i+3)  # Next 3 wires for b
        
        # Apply CCNOT (Toffoli) gates to compute AND
        for i in range(3):
            qml.Toffoli(wires=[i, i+3, i+6])  # ancilla at i+6
        
        # Measure the ancillary qubits (last 3 wires)
        return qml.sample(wires=[6, 7, 8])
    
    samples = circuit()
    
    # If we're getting a single sample array, convert it properly
    if len(samples.shape) == 1:
        # Single sample case - reshape to list of samples
        samples = samples.reshape(-1, 3)
    
    # Convert samples to bitstrings
    bitstring_samples = []
    for sample in samples:
        bitstring = ''.join(str(int(bit)) for bit in sample)
        bitstring_samples.append(bitstring)
    
    # Count occurrences of each bitstring
    counts = Counter(bitstring_samples)
    total = sum(counts.values())
    
    # Normalize to get probabilities
    prob_dist = {bitstring: count/total for bitstring, count in counts.items()}
    
    return prob_dist
