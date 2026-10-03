# EVAL_META: task_id=55, framework=pennylane, class=1
import pennylane as qml
from collections import Counter

def or_gate(a, b):
    dev = qml.device("default.qubit", wires=9, shots=None)
    
    @qml.qnode(dev)
    def circuit():
        # Initialize registers: 3 for a, 3 for b, 3 for ancillary
        a_bits = [int(bit) for bit in format(a, '03b')]
        b_bits = [int(bit) for bit in format(b, '03b')]
        
        # Apply X gates to flip bits that are 0 (since we want to represent 0 as |1⟩ initially)
        for i in range(3):
            if a_bits[2-i] == 0:
                qml.PauliX(wires=i)
            if b_bits[2-i] == 0:
                qml.PauliX(wires=i+3)
        
        # Apply CCNOT (Toffoli) gates for AND operation between corresponding bits
        for i in range(3):
            qml.Toffoli(wires=[i, i+3, i+6])  # Control on a[i] and b[i], target on ancilla[i]
        
        # Flip all ancillary bits to get OR instead of AND
        for i in range(3):
            qml.PauliX(wires=i+6)
        
        # Measure the ancillary register
        return qml.sample(wires=[6, 7, 8])
    
    # Sample multiple times to get probability distribution
    samples = circuit()
    if len(samples.shape) == 1:
        samples = samples.reshape(-1, 3)
    
    # Count occurrences of each bit string
    bit_strings = [''.join(map(str, sample)) for sample in samples]
    counts = Counter(bit_strings)
    
    # Convert to probabilities
    total = sum(counts.values())
    prob_dist = {key: value / total for key, value in counts.items()}
    
    return prob_dist
